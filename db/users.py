"""Users db model"""

from sqlite_database import blob, text
from .helpers import boolean

USER_SCHEMA = [
    text("id").primary(),
    text("username").unique(),
    text("password"),
    text("email").unique(),
    blob("photo").allow_null(),
    text("full_name").allow_null(),
    boolean("is_active").default(True),
    text('role').default('user')
]

VAL_VISIBILITY = (
    "username",
    "id",
    "email",
    "photo",
    "full_name",
    "is_active",
    "role"
)
