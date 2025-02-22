from sqlite_database import integer, text, real
from ..helpers import boolean

SCHEMA = [
    text("id").primary(),
    text("email"),
    text("full_name"),
    integer("phone_number"),
    text("title"),
    text("message"),
    boolean("is_read").default(False),
    real("created_at"),
]

VAL_REQUIRED = (
    "email",
    "full_name",
    "phone_number",
    "title",
    "message",
)
