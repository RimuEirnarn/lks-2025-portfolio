from flask_wtf import FlaskForm
from wtforms import FileField, StringField, SubmitField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


class PortfolioForm(FlaskForm):
    category = StringField("Category", [DataRequired()])
    title = StringField("Title", [DataRequired()])
    sort_description = StringField("Sort description")
    tags = StringField("Tags")
    thumbnail = FileField("Thumbnail")
    content = TextAreaField("Content", [DataRequired()])
    cover = FileField("Cover")
    meta_title = StringField("Meta title")
    meta_description = StringField("Meta description")
    is_active = BooleanField("Is active")
    slug = StringField("Slug")

    submit = SubmitField("Save")
