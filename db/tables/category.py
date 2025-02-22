from sqlite_database import text, blob
from ..helpers import boolean

SCHEMA = [
    text("id").primary(),
    text("title"),
    text("sort_description"),
    blob("thumbnail").allow_null(),
    boolean("is_active"),
]
