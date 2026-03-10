"""
Database connection setup - Phase 2
Configures Tortoise ORM with SQLite (dev) or PostgreSQL (production)
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment, default to SQLite for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://db.sqlite3")

# Tortoise ORM with asyncpg uses "postgres://" scheme, not "postgresql://"
# Railway provides "postgresql://" so we need to convert it
if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgres://", 1)

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["backend.models"],
            "default_connection": "default",
        }
    },
}
