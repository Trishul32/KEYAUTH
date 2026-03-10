"""
Database connection setup - Phase 2
Configures Tortoise ORM with SQLite (dev) or PostgreSQL (production)
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Get database URL from environment, default to SQLite for local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://db.sqlite3")

# Tortoise ORM with asyncpg uses "postgres://" or "asyncpg://" scheme
# No conversion needed - Railway provides postgres:// which works with Tortoise

TORTOISE_ORM = {
    "connections": {"default": DATABASE_URL},
    "apps": {
        "models": {
            "models": ["backend.models"],
            "default_connection": "default",
        }
    },
}
