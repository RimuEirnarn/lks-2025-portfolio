"""Helpers functions"""

from uuid import uuid4

from sqlite_database.column import create_calls

boolean = create_calls("boolean", ["boolean"])


def generate_id():
    """Generate UUID"""
    return str(uuid4())
