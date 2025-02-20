"""Base Database"""

from os import environ
from uuid import UUID

from werkzeug.security import generate_password_hash
from sqlite_database import Database
from sqlite_database.errors import DatabaseExistsError
from dotenv import load_dotenv

from .users import USER_SCHEMA, VAL_VISIBILITY as USER_DATA_VISIBILITY
from .portfolio import PORTFOLIO_SCHEMA
from .category import CATEGORY_SCHEMA
from .contactform import CONTACT_FORM_SCHEMA
from .content import CONTENT_SCHEMA

load_dotenv()
DB_PATH = environ.get("DB_PATH", "transient/db.sqlite3")

db = Database(DB_PATH)

# ! Content type cannot use Enum due to sqlite_database limitation for enum.

try:
    db.check_table("users")
    users_tbl = db.create_table("users", USER_SCHEMA)
    portfolio_tbl = db.create_table("portfolio", PORTFOLIO_SCHEMA)
    category_tbl = db.create_table("category", CATEGORY_SCHEMA)
    contact_form_tbl = db.create_table("contact_form", CONTACT_FORM_SCHEMA)
    content_tbl = db.create_table("content", CONTENT_SCHEMA)
    users_tbl.insert(
        {
            "id": str(UUID(int=0)),
            "username": environ.get("ADMIN_USERNAME", "admin"),
            "full_name": "System Administrator",
            "password": generate_password_hash(environ.get("ADMIN_PASSWORD", "admin")),
            "email": "admin@localhost.com",
            "role": 'admin'
        }
    )
except DatabaseExistsError:
    users_tbl = db.table("users")
    posts_tbl = db.table("posts")
    portfolio_tbl = db.table("portfolio")
    category_tbl = db.table("category")
    contact_form_tbl = db.table("contact_form")
    content_tbl = db.table("content")
