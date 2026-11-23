
from expense_server.database.connection import get_connection


# 1. ADD EXPENSE
def add_expense(
    amount: float,
    category: str,
    description: str,
    expense_date: str,
    payment_method: str | None = None
) -> int:
    """Add a new expense and return its ID."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            INSERT INTO expenses (
                amount,
                category,
                description,
                expense_date,
                payment_method
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (amount, category, description, expense_date, payment_method)
        )

        connection.commit()
        return cursor.lastrowid

    finally:
        connection.close()


# 2. EDIT EXPENSE
def edit_expense(
    expense_id: int,
    amount: float,
    category: str,
    description: str,
    expense_date: str,
    payment_method: str | None = None
) -> bool:
    """Edit an existing expense using its ID."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            UPDATE expenses
            SET amount = ?,
                category = ?,
                description = ?,
                expense_date = ?,
                payment_method = ?
            WHERE id = ?
            """,
            (
                amount,
                category,
                description,
                expense_date,
                payment_method,
                expense_id
            )
        )

        connection.commit()
        return cursor.rowcount > 0

    finally:
        connection.close()


# 3. LIST ALL EXPENSES
def list_all_expenses() -> list[dict]:
    """Retrieve all expenses."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT *
            FROM expenses
            ORDER BY expense_date DESC, id DESC
            """
        )

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


# 4. LIST EXPENSES BY DATE RANGE
def list_expenses_by_date_range(
    start_date: str,
    end_date: str
) -> list[dict]:
    """Retrieve expenses between two dates, inclusive."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT *
            FROM expenses
            WHERE expense_date >= ?
              AND expense_date <= ?
            ORDER BY expense_date DESC, id DESC
            """,
            (start_date, end_date)
        )

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


# 5. SUMMARISE EXPENSES BY CATEGORY
def summarize_expenses_by_category() -> list[dict]:
    """Return total spending and expense count for each category."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                category,
                SUM(amount) AS total_amount,
                COUNT(*) AS expense_count
            FROM expenses
            GROUP BY category
            ORDER BY total_amount DESC
            """
        )

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


# 6. SUMMARISE EXPENSES BY CATEGORY WITHIN DATE RANGE
def summarize_expenses_by_category_and_date_range(
    start_date: str,
    end_date: str
) -> list[dict]:
    """Return category-wise spending within a date range, inclusive."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            SELECT
                category,
                SUM(amount) AS total_amount,
                COUNT(*) AS expense_count
            FROM expenses
            WHERE expense_date >= ?
              AND expense_date <= ?
            GROUP BY category
            ORDER BY total_amount DESC
            """,
            (start_date, end_date)
        )

        return [dict(row) for row in cursor.fetchall()]

    finally:
        connection.close()


# 7. DELETE EXPENSE
def delete_expense(expense_id: int) -> bool:
    """Delete an expense using its ID."""

    connection = get_connection()

    try:
        cursor = connection.execute(
            """
            DELETE FROM expenses
            WHERE id = ?
            """,
            (expense_id,)
        )

        connection.commit()
        return cursor.rowcount > 0

    finally:
        connection.close()
