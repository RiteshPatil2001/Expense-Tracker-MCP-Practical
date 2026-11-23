
from datetime import date
import math

from expense_server.database import queries
from expense_server.database import category_config


# ------------------------------------------
# VALIDATION HELPERS
# ------------------------------------------

def validate_amount(amount: float) -> None:
    """Validate an expense amount."""

    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        raise ValueError("Amount must be a valid number.")

    if not math.isfinite(amount) or amount <= 0:
        raise ValueError("Amount must be greater than zero.")


def validate_expense_id(expense_id: int) -> None:
    """Validate expense ID."""

    if isinstance(expense_id, bool) or not isinstance(expense_id, int):
        raise ValueError("Expense ID must be an integer.")

    if expense_id <= 0:
        raise ValueError("Expense ID must be greater than zero.")


def validate_date(expense_date: str) -> None:
    """Validate date in YYYY-MM-DD format."""

    try:
        date.fromisoformat(expense_date)
    except (ValueError, TypeError):
        raise ValueError("Date must be in YYYY-MM-DD format.")


def validate_date_range(start_date: str, end_date: str) -> None:
    """Validate start and end dates."""

    validate_date(start_date)
    validate_date(end_date)

    if start_date > end_date:
        raise ValueError("Start date cannot be later than end date.")


# ------------------------------------------
# 1. ADD EXPENSE
# ------------------------------------------

def add_expense(
    amount: float,
    category: str,
    description: str,
    expense_date: str,
    payment_method: str | None = None
) -> int:

    validate_amount(amount)
    category = category_config.validate_category(category)
    validate_date(expense_date)

    expense_id = queries.add_expense(
        amount=amount,
        category=category.strip(),
        description=description or "",
        expense_date=expense_date,
        payment_method=payment_method
    )

    return expense_id


# ------------------------------------------
# 2. EDIT EXPENSE
# ------------------------------------------

def edit_expense(
    expense_id: int,
    amount: float,
    category: str,
    description: str,
    expense_date: str,
    payment_method: str | None = None
) -> bool:

    validate_expense_id(expense_id)
    validate_amount(amount)
    category = category_config.validate_category(category)
    validate_date(expense_date)

    return queries.edit_expense(
        expense_id=expense_id,
        amount=amount,
        category=category.strip(),
        description=description or "",
        expense_date=expense_date,
        payment_method=payment_method
    )


# ------------------------------------------
# 3. LIST ALL EXPENSES
# ------------------------------------------

def list_all_expenses() -> list[dict]:
    return queries.list_all_expenses()


# ------------------------------------------
# 4. LIST EXPENSES BY DATE RANGE
# ------------------------------------------

def list_expenses_by_date_range(
    start_date: str,
    end_date: str
) -> list[dict]:

    validate_date_range(start_date, end_date)

    return queries.list_expenses_by_date_range(
        start_date=start_date,
        end_date=end_date
    )


# ------------------------------------------
# 5. SUMMARISE EXPENSES BY CATEGORY
# ------------------------------------------

def summarize_expenses_by_category() -> list[dict]:
    return queries.summarize_expenses_by_category()


# ------------------------------------------
# 6. SUMMARISE BY CATEGORY AND DATE RANGE
# ------------------------------------------

def summarize_expenses_by_category_and_date_range(
    start_date: str,
    end_date: str
) -> list[dict]:

    validate_date_range(start_date, end_date)

    return queries.summarize_expenses_by_category_and_date_range(
        start_date=start_date,
        end_date=end_date
    )


# ------------------------------------------
# 7. DELETE EXPENSE
# ------------------------------------------

def delete_expense(expense_id: int) -> bool:

    validate_expense_id(expense_id)

    return queries.delete_expense(expense_id)
