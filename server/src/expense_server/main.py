
import sys

from fastmcp import FastMCP

from expense_server.database.schema import initialize_database
from expense_server.tools.expense_tools import register_expense_tools


mcp = FastMCP("Expense Tracker")

register_expense_tools(mcp)


def main() -> None:
    """Initialize the database and start the MCP server."""

    initialize_database()

    print(
        "Expense Tracker MCP Server starting...",
        file=sys.stderr,
        flush=True
    )

    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
