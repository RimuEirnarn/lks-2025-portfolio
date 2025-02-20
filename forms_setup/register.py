"""Register"""

from flask_wtf import FlaskForm
from wtforms import EmailField, StringField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, EqualTo, Email


class Register(FlaskForm):
    """Register"""

    full_name = StringField("Your full name", [DataRequired()])
    username = StringField("Your username", [DataRequired()])
    email = EmailField("Your email", [DataRequired(), Email()])
    photo = FileField("photo")

    password = PasswordField("Password", [DataRequired()])
    retype = PasswordField(
        "Retype your password",
        [DataRequired(), EqualTo("password", "Password must match")],
    )

    submit = SubmitField("Register")
