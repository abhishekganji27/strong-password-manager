from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length


# Create a form class
class GenPwdForm(FlaskForm):
    user = StringField("Enter the User Name")
    appli_name = StringField("Enter the Application Name", validators=[DataRequired()])
    appli_user_name = StringField("Enter the User Name for the application", validators=[DataRequired()])
    password = StringField("Enter the Password for the application", validators=[DataRequired()])
    generate = SubmitField("Generate")
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


# Create a Search Form
class SearchForm(FlaskForm):
    search_query = StringField("Search for a Password", validators=[DataRequired()])
    submit = SubmitField("Submit")