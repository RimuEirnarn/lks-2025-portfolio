"""Helpers functions"""

from uuid import uuid4

from sqlite_database.column import BuilderColumn


def boolean(name: str) -> BuilderColumn:
    """Create boolean column"""
    return BuilderColumn().set_type("boolean")(name)


def generate_id():
    """Generate UUID"""
    return str(uuid4())
