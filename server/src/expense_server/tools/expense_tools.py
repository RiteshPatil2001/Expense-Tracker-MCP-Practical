
from fastmcp import FastMCP

from expense_server.services import expense_service


def register_expense_tools(mcp: FastMCP) -> None:
    """Register all expense-management tools with the MCP server."""

    @mcp.tool()
    def add_expense(
        amount: float,
        category: str,
        expense_date: str,
        description: str = "",
        payment_method: str | None = None
    ) -> dict:
        """
        Add a new expense.

        Args:
            amount: Expense amount. Must be greater than zero.
            category: Expense category, such as Food, Travel or Shopping.
            expense_date: Expense date in YYYY-MM-DD format.
            description: Optional details about the expense.
            payment_method: Optional method such as Cash, UPI or Card.
        """
        expense_id = expense_service.add_expense(
            amount=amount,
            category=category,
            description=description,
            expense_date=expense_date,
            payment_method=payment_method
        )

        return {
            "success": True,
            "message": "Expense added successfully.",
            "expense_id": expense_id
        }

    @mcp.tool()
    def edit_expense(
        expense_id: int,
        amount: float,
        category: str,
        expense_date: str,
        description: str = "",
        payment_method: str | None = None
    ) -> dict:
        """
        Edit an existing expense using its expense ID.

        Args:
            expense_id: ID of the expense to edit.
            amount: Updated expense amount.
            category: Updated expense category.
            expense_date: Updated date in YYYY-MM-DD format.
            description: Updated description.
            payment_method: Updated payment method.
        """
        updated = expense_service.edit_expense(
            expense_id=expense_id,
            amount=amount,
            category=category,
            description=description,
            expense_date=expense_date,
            payment_method=payment_method
        )

        if not updated:
            return {
                "success": False,
                "message": f"Expense with ID {expense_id} was not found."
            }

        return {
            "success": True,
            "message": "Expense updated successfully.",
            "expense_id": expense_id
        }

    @mcp.tool()
    def list_all_expenses() -> dict:
        """Retrieve all expenses."""

        expenses = expense_service.list_all_expenses()

        if not expenses:
            return {
                "success": True,
                "message": "No expenses found.",
                "expenses": []
            }

        return {
            "success": True,
            "message": f"Found {len(expenses)} expenses.",
            "expenses": expenses
        }

    @mcp.tool()
    def list_expenses_by_date_range(
        start_date: str,
        end_date: str
    ) -> dict:
        """Retrieve expenses within a date range."""

        expenses = expense_service.list_expenses_by_date_range(
            start_date,
            end_date
        )

        if not expenses:
            return {
                "success": True,
                "message": (
                    f"No expenses found between "
                    f"{start_date} and {end_date}."
                ),
                "expenses": []
            }

        return {
            "success": True,
            "message": f"Found {len(expenses)} expenses.",
            "expenses": expenses
        }

    @mcp.tool()
    def summarize_expenses_by_category() -> dict:
        """Summarize expenses category-wise."""

        summary = expense_service.summarize_expenses_by_category()

        if not summary:
            return {
                "success": True,
                "message": "No expenses available for category-wise summary.",
                "summary": []
            }

        return {
            "success": True,
            "message": "Category-wise expense summary retrieved.",
            "summary": summary
        }

    @mcp.tool()
    def summarize_expenses_by_category_and_date_range(
        start_date: str,
        end_date: str
    ) -> list[dict]:
        """
        Summarize category-wise spending within a date range.

        Args:
            start_date: Starting date in YYYY-MM-DD format.
            end_date: Ending date in YYYY-MM-DD format.
        """
        return expense_service.summarize_expenses_by_category_and_date_range(
            start_date=start_date,
            end_date=end_date
        )

    @mcp.tool()
    def delete_expense(expense_id: int) -> dict:
        """
        Delete an expense using its ID.

        Args:
            expense_id: ID of the expense to delete.
        """
        deleted = expense_service.delete_expense(expense_id)

        if not deleted:
            return {
                "success": False,
                "message": f"Expense with ID {expense_id} was not found."
            }

        return {
            "success": True,
            "message": "Expense deleted successfully.",
            "expense_id": expense_id
        }
