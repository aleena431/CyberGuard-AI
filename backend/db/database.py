import os
from contextlib import contextmanager

import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_database_url() -> str:
    """Return the configured PostgreSQL connection URL."""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise RuntimeError("DATABASE_URL is missing. Check your .env file.")
    return database_url


@contextmanager
def get_db_connection():
    """Open a database connection and close it automatically."""
    with psycopg.connect(get_database_url()) as connection:
        yield connection


def check_database() -> bool:
    """Return True when PostgreSQL responds to a simple query."""
    with get_db_connection() as connection:
        connection.execute("SELECT 1")
    return True
