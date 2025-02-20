from typing import NotRequired
from flask_wtf import FlaskForm
from wtforms import BooleanField, BooleanField, FileField, StringField, SubmitField


class ContentForm(FlaskForm):
    title = StringField("Category title", [NotRequired()])
    sort_description = StringField("Sort description")
    thumbnail = FileField("Thumbnail")

    is_active = BooleanField("Is active")
    submit = SubmitField("Save")
