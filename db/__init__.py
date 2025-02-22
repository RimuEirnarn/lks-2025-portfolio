"""Base Database"""

import os
import importlib
import pkgutil
from os.path import join as path_join
from uuid import UUID
# from werkzeug.security import generate_password_hash
from sqlite_database import Database, Table
from sqlite_database.errors import DatabaseExistsError
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.environ.get("DB_PATH", "transient/db.sqlite3")

db = Database(DB_PATH)

# Update as you see fit.

users_tbl: Table
category_tbl: Table
content_tbl: Table
portfolio_tbk: Table
contactform_tbl: Table

#

# Dynamically import schema modules
package = __package__  # 'db'
schema_modules = [
    name for _, name, _ in pkgutil.iter_modules([path_join(os.path.dirname(__file__), 'tables')])
    if not name.startswith("_") and name != "seeder"
]

# Dictionary to store created table instances
known_tables: dict[str, Table] = {}
__all__ = ['db', 'known_tables', 'DB_PATH']

try:
    # **Step 1: Create Tables First**
    for module_name in schema_modules:
        module = importlib.import_module(f"{package}.tables.{module_name}")
        schema_attr = "SCHEMA"

        if hasattr(module, schema_attr):
            schema = getattr(module, schema_attr)
            known_tables[module_name] = db.create_table(module_name, schema)

    # **Step 2: Seed Data After All Tables Exist**
    seeder_modules = [
        name for _, name, _ in pkgutil.iter_modules([os.path.join(os.path.dirname(__file__), "seeder")])
        if not name.startswith("_")
    ]

    for seeder_name in seeder_modules:
        seeder_module = importlib.import_module(f"{package}.seeder.{seeder_name}")
        if hasattr(seeder_module, "seed") and callable(seeder_module.seed):
            print(f"Seeding {seeder_name}...")
            seeder_module.seed(known_tables)  # Pass the table dictionary

    # # Ensure admin user exists
    # users_tbl = tables.get("users")
    # if users_tbl:
    #     users_tbl.insert(
    #         {
    #             "id": str(UUID(int=0)),
    #             "username": os.environ.get("ADMIN_USERNAME", "admin"),
    #             "full_name": "System Administrator",
    #             "password": generate_password_hash(os.environ.get("ADMIN_PASSWORD", "admin")),
    #             "email": "admin@localhost.com",
    #             "role": "admin",
    #         }
    #     )

except DatabaseExistsError:
    for module_name in schema_modules:
        known_tables[module_name] = db.table(module_name)
        globals()[f"{module_name}_tbl"] = known_tables[module_name]
        __all__.append(f"{module_name}_tbl")