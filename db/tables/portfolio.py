from sqlite_database import real, text
from ..helpers import boolean


SCHEMA = [
    text("id").primary(),
    text("author").foreign("users/id"),
    text("category").foreign("category/id"),
    text("title"),
    text("sort_description"),
    text("content"),
    boolean("is_active"),
    real("created_at"),
    real("updated_at"),
    text("slug"),
    text("tags"),
    text("cover").allow_null(),
    text("thumbnail").allow_null(),
    text("meta_title"),
    text("meta_tag"),
    text("meta_description"),
]
