from sqlite_database import text
from ..helpers import boolean

SCHEMA = [
    text("id").primary(),
    text("title"),
    text("sort_description"),
    text("thumbnail").allow_null(),
    boolean("is_active"),
]
