from sqlite_database import blob, blob, real, text
from .helpers import boolean


PORTFOLIO_SCHEMA = [
    text("id").primary(),
    text("author").foreign("users/id"),
    text("category").foreign("category/id"),
    text("title"),
    text("sort_description"),
    text("content"),
    boolean("is_active"),
    real("created_at"),
    real("updated_at"),
    text("slugs"),
    text("tags"),
    blob("cover").allow_null(),
    blob("thumbnail").allow_null(),
    text("meta_title"),
    text("meta_tag"),
    text("meta_description"),
]
