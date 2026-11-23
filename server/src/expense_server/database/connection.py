
import os
import sqlite3
from pathlib import Path


def get_database_path() -> Path:
    """
    Resolve the SQLite database path.

    Relative paths are resolved from the project root,
    not from the current terminal directory.
    """

    project_root = Path(__file__).resolve().parents[4]

    configured_path = os.getenv(
        "DATABASE_PATH",
        "server/data/expenses.db"
    )

    database_path = Path(configured_path)

    if not database_path.is_absolute():
        database_path = project_root / database_path

    database_path.parent.mkdir(parents=True, exist_ok=True)

    return database_path


def get_connection() -> sqlite3.Connection:
    """
    Create and return a SQLite database connection.
    """

    database_path = get_database_path()

    connection = sqlite3.connect(
        database_path,
        timeout=30
    )

    connection.row_factory = sqlite3.Row

    # Enable foreign key constraints.
    connection.execute("PRAGMA foreign_keys = ON")

    return connection
