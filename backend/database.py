"""
Database connection setup - Phase 2
Configures Tortoise ORM with SQLite (dev) or PostgreSQL (production)
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment, default to SQLite for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://db.sqlite3")

# Fix for some cloud providers that use "postgres://" instead of "postgresql://"
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["backend.models"],
            "default_connection": "default",
        }
    },
}
