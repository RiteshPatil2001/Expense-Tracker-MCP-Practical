
from expense_server.database.connection import get_connection


def initialize_database() -> None:
    """
    Create the expenses table if it does not already exist.
    """

    connection = get_connection()

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                description TEXT,
                expense_date TEXT NOT NULL,
                payment_method TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_expenses_date
            ON expenses(expense_date)
            """
        )

        connection.commit()

    finally:
        connection.close()
