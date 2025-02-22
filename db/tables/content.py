from enum import Enum, StrEnum

from sqlite_database import text, real

# ? To mitigate sqlite_database limitation for enum, we have to make certain quirks/changes so we can emulate enums within text scale
# ? This is a workaround for sqlite_database limitation for enum


class ContentType(StrEnum):
    HEADER = "header"
    ABOUT_ME = "about_me"
    CONTACT_ME = "contact_me"
    EXPERTISE = "expertise"
    EXPERIENCE = "experience"
    TESTIMONIAL = "testimonial"

def validate_enum(value, enum: Enum):
    return any((value == member) for member in enum.__member__)

SCHEMA = [
    text("id").primary(),
    text("author").foreign("users/id"),
    text("content_type"),
    text("title"),
    text("sub_title"),
    text("sort_description"),
    text("content"),
    text("thumbnail"),
    real("score"),
    real("created_at"),
    real("updated_at"),
]