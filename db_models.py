from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_login import UserMixin




#Create a flask instance
app = Flask(__name__)

# SQLite database 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passwords.db'

# MySQL database 
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{username}:{password}@localhost/{database_name}'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/passwords_database'

# Secret Key idky
app.config['SECRET_KEY'] = "sk123"

db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Create model
class Passwords(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    # user = db.Column(db.String(200), nullable = False)
    appli_name = db.Column(db.String(200), nullable = False) 
    appli_user_name = db.Column(db.String(200), nullable = False) 
    password = db.Column(db.String(200), nullable = False)
    date_added = db.Column(db.DateTime, default=datetime.now()) 
    last_updated = db.Column(db.DateTime, default=datetime.now()) 
    
    # Foreign key to link users (refer to primary key of users)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))


# Create Users model
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), unique=True, nullable = False)
    password = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.now()) 
    # Users can have many passwords
    pwds = db.relationship('Passwords', backref='creator')
    # backref is used to access Passwords table data 


