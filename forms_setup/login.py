"""Login"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    """Login form"""
    username = StringField("Your username", [InputRequired()])
    password = PasswordField("Password", [InputRequired()])
    remember = BooleanField("Remember me")

    submit = SubmitField("Submit")