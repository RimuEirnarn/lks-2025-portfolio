"""Global helper"""

from functools import wraps
from typing import NamedTuple
from flask import render_template
from flask_login import current_user
from flask_wtf import CSRFProtect
from db import users_tbl, USER_DATA_VISIBILITY


def is_admin(func):
    """Is user an admin?"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if current_user.role != "admin":
            return render_template("unathorized.html"), 403
        return func(*args, **kwargs)

    return wrapper


class User(NamedTuple):
    """User class"""

    id: str
    username: str
    display_name: str
    role: str

    def is_authenticated(self):
        """Is user authenticated?"""
        return True

    def is_active(self):
        """Is user active?"""
        return True

    def is_anonymous(self):
        """Is user anonymous?"""
        return False

    def get_id(self):
        """Get user ID"""
        return self.id

    @classmethod
    def load(cls, **kwargs):
        """Load user based on USER_VISIBILITY"""
        return cls(
            **{
                key: value
                for key, value in kwargs.items()
                if key in USER_DATA_VISIBILITY
            }
        )


def load_user(uid):
    """Load user from UID"""
    return User.load(**users_tbl.select_one({"id": id}))


csrf = CSRFProtect()
