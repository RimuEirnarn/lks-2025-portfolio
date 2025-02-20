from flask_wtf import FlaskForm
from wtforms import BooleanField, BooleanField, FileField, StringField, SubmitField
from wtforms.validators import DataRequired


class CategoryForm(FlaskForm):
    title = StringField("Category title", [DataRequired()])
    sort_description = StringField("Sort description")
    thumbnail = FileField("Thumbnail")

    is_active = BooleanField("Is active")
    submit = SubmitField("Save")
