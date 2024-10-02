from flask import Flask, render_template, flash, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

#Create a flask instance
app = Flask(__name__)

# SQLite database 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passwords.db'

# MySQL database 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/passwords_database'

# Secret Key
app.config['SECRET_KEY'] = "sk123"

db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Flask Login Stuff

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Create model
class Passwords(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    user = db.Column(db.String(200), nullable = False)
    appli_name = db.Column(db.String(200), nullable = False, unique=True) 
    appli_user_name = db.Column(db.String(200), nullable = False) 
    password = db.Column(db.String(200), nullable = False)
    date_added = db.Column(db.DateTime, default=datetime.now()) 
    last_updated = db.Column(db.DateTime, default=datetime.now()) 

# Create Users model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), unique=True, nullable = False)
    password = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.now()) 

# Creation of the database tables within the application context.
with app.app_context():
    db.create_all()

# Create a form class
class GenPwdForm(FlaskForm):
    user = StringField("Enter the User Name", validators=[DataRequired()])
    appli_name = StringField("Enter the Application Name", validators=[DataRequired()])
    appli_user_name = StringField("Enter the User Name for the application", validators=[DataRequired()])
    password = PasswordField("Enter the Password for the application", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a Registration form class
class RegistrationForm(FlaskForm):
    username = StringField("Enter a Username", validators=[DataRequired()])
    password = PasswordField("Enter a Password", validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match!')])
    confirm_password = PasswordField("Re-enter the Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

# Create a login form
class LoginForm(FlaskForm):
    username = StringField("Enter a Username", validators=[DataRequired()])
    password = PasswordField("Enter a Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


# Create a route decorator
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard.html")

# Custom Error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Create Generate Password Form Page
@app.route('/passwords', methods=['GET', 'POST'])
@login_required
def show_passwords():
    all_passwords = Passwords.query.order_by(Passwords.date_added)
    return render_template("show_passwords.html",
                            all_passwords = all_passwords)

@app.route('/users', methods=['GET', 'POST'])
@login_required
def show_users():
    all_users = Users.query.order_by(Users.date_created)
    return render_template("show_users.html",
                            all_users = all_users)

@app.route('/create-password', methods=['GET', 'POST'])
@login_required
def create_passwords():
    user = None
    appli_name = None
    appli_user_name = None
    password = None
    form = GenPwdForm()

    # Validate form
    if form.validate_on_submit():
        # user_name = form.user_name.data
        # form.user_name.data = ''
        # appli_name = form.appli_name.data
        # form.appli_name.data = ''
        # appli_user_name = form.appli_user_name.data
        # form.appli_user_name.data = ''
        result = Passwords.query.filter_by(appli_name=form.appli_name.data).first()
        if result is None:
            result = Passwords(
                user = form.user.data,
                appli_name = form.appli_name.data,
                appli_user_name = form.appli_user_name.data,
                password = form.password.data,
                )
            db.session.add(result)
            db.session.commit()
        
        user = form.user.data
        form.user.data = ''  
        appli_name = form.appli_name.data
        form.appli_name.data = ''
        appli_user_name = form.appli_user_name.data
        form.appli_user_name.data = ''
        password = form.password.data
        form.password.data = ''  
        
        flash("Password Created!")
        return redirect(url_for('show_passwords'))
    
    return render_template("passwords_form.html",
                            user = user,
                            appli_name=appli_name, 
                            appli_user_name=appli_user_name,
                            password = password,
                            form = form)

# Update Database record (Passwords)
@app.route('/update-password/<int:id>', methods=['GET', 'POST'])
@login_required
def update_password(id):
    form = GenPwdForm()
    # Row to update
    old_record = Passwords.query.get_or_404(id)
    if request.method == "POST":
        old_record.appli_name=request.form['appli_name']
        old_record.appli_user_name=request.form['appli_user_name']
        old_record.password=request.form['password']
        old_record.last_updated=datetime.now()
        try:
            db.session.commit()
            flash("Details Updated Successfully!")
            return render_template("update_password.html",
                                   form=form,
                                   old_record=old_record)

        except:
            flash("Error!")
            return render_template("update_password.html",
                                   form=form,
                                   old_record=old_record)
    else:
        return render_template("update_password.html",
                                form=form,
                                old_record=old_record)
    
@app.route('/delete_password/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_password(id):

    record_to_delete = Passwords.query.get_or_404(id)

    try:
        db.session.delete(record_to_delete)
        db.session.commit()
        flash("Password Deleted Successfully!")
        return redirect(url_for('show_passwords'))
        
    except:
        flash("Error!")
        return redirect(url_for('update_password', id=id))


@app.route('/login', methods=['POST', 'GET'])
def login():
    
    form = LoginForm()
    if form.validate_on_submit():
        logged_user = Users.query.filter_by(username=form.username.data).first()
        if logged_user: 
            #check the password hash
            # if check_password_hash(logged_user.password_hash, form.password.data):
            if logged_user.password == form.password.data:
                # Flask Login stuff to login the user.
                login_user(logged_user)
                return redirect(url_for('dashboard'))
            else:
                flash("Wrong password! Try again...")
                # return redirect(url_for('login'))
        else:
            flash("User doesn't exist! Try again...")
            return redirect(url_for('registration'))
    
    return render_template("login.html", form=form)


@app.route('/registration', methods=['POST', 'GET'])
def registration():

    form=RegistrationForm()

    if form.validate_on_submit():
        result = Users.query.filter_by(username=form.username.data).first()
        if result is None: 
            result=Users(   
                username = form.username.data,
                password = form.password.data,
            )
            try:
                db.session.add(result)
                db.session.commit()
                flash("You have registered successfully!")
                return redirect(url_for('login'))

            except:
                flash("Something went wrong!")
                return redirect(url_for('registration', form=form))
        else:
            flash("You already have an account! Login...")
            return redirect(url_for('login'))


    return render_template("registration.html", form=form)

#Create logout function
@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out!")
    return redirect(url_for('login'))