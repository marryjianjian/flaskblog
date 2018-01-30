from flask_wtf import FlaskForm as Form
from wtforms import BooleanField, StringField, PasswordField, validators
from wtforms import TextAreaField, SubmitField


class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=3, max=30)])
    password = PasswordField('Password', [validators.DataRequired()])


class RegisterForm(Form):
    username = StringField('Username', [validators.Length(3, 30)])
    email = StringField('Email', [validators.Required(), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])
