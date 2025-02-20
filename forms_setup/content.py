from flask_wtf import FlaskForm
from wtforms import (
    FileField,
    IntegerField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, EqualTo


class ContentForm(FlaskForm):
    title = StringField("Category title", [(DataRequired())])
    content_type = StringField("Content type")
    sort_description = StringField("Sort description")
    thumbnail = FileField("Thumbnail")
    sub_title = StringField("Sub title")
    content = TextAreaField("Content")
    score = IntegerField("Score")

    submit = SubmitField("Save")
