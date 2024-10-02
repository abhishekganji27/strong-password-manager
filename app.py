from flask import Flask, render_template, flash, redirect, url_for, request
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from forms import LoginForm, RegistrationForm, GenPwdForm, SearchForm
from db_models import *
from password_gen_logic import generate_password

# Flask Login Stuff

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))



# Creation of the database tables within the application context.
with app.app_context():
    db.create_all()



# Create a route decorator
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/dashboard/update-user/<int:id>", methods=['GET', 'POST'])
@login_required
def update_user(id):
    return render_template("dashboard.html")


# Custom Error pages
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

# Show the passwords 
@app.route('/passwords', methods=['GET', 'POST'])
@login_required
def show_passwords():
    all_passwords = Passwords.query\
        .filter_by(creator_id=current_user.id)\
        .order_by(Passwords.date_added)
    return render_template("show_passwords.html",
                            all_passwords = all_passwords)

@app.route('/users', methods=['GET', 'POST'])
@login_required
def show_users():
    all_users = Users.query.order_by(Users.date_created)
    return render_template("show_users.html",
                            all_users = all_users)

# Create the password record in Passwords db.
@app.route('/create-password', methods=['GET', 'POST'])
@login_required
def create_passwords():
    # user = None
    appli_name = ''
    appli_user_name = ''
    password = ''
    form = GenPwdForm()

    # Validate form
    if form.validate_on_submit():
        # Check if Generate button is clicked 
        if form.generate.data:
            # Generate a password
            password = generate_password()
            return render_template("passwords_form.html",
                            appli_name= form.appli_name.data, 
                            appli_user_name=form.appli_user_name.data,
                            password = password,
                            form = form)
        
        result = Passwords.query.filter_by\
            (appli_name = form.appli_name.data,\
            appli_user_name = form.appli_user_name.data,\
              creator_id = current_user.id).first()
        if result is None:
            result = Passwords(
                creator_id = current_user.id,
                appli_name = form.appli_name.data,
                appli_user_name = form.appli_user_name.data,
                password = form.password.data,
                )
            db.session.add(result)
            db.session.commit()
        
            appli_name = form.appli_name.data
            form.appli_name.data = ''
            appli_user_name = form.appli_user_name.data
            form.appli_user_name.data = ''
            password = form.password.data
            form.password.data = ''  
            
            flash("Password Created!")
            return redirect(url_for('show_passwords'))
        else:
            flash("Password Exists! Would you like to Update it?")
            return redirect(url_for('update_password', id=result.id))

    return render_template("passwords_form.html",
                            appli_name=appli_name, 
                            appli_user_name=appli_user_name,
                            password = password,
                            form = form)


# Pass stuff to Navbar (which is An Extended Base file)
@app.context_processor
def base():
    form=SearchForm()
    return dict(form=form)

# Perform search queries on passwords
@app.route('/search-password', methods=['POST'])
@login_required
def search_password():
    form = SearchForm()
    if form.validate_on_submit():
        # Get the search query string
        search_query = form.search_query.data

        # Query the Passwords Database for matches
        matches = Passwords.query\
            .filter(Passwords.appli_name.like('%'+search_query+'%') |\
                Passwords.appli_user_name.like('%'+search_query+'%'))\
                .filter_by(creator_id = current_user.id)\
                .order_by(Passwords.date_added.desc()).all()
        return render_template("search_password.html", search_results = matches, search_query=search_query)

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
        old_record.last_updated=datetime.now()
       
        if form.generate.data:
            old_record.password=generate_password()
            return render_template("update_password.html",
                                form=form,
                                old_record=old_record)
        else:
            old_record.password=request.form['password']
        
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