
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient


# Locate the repository root.
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Load environment variables from the root .env file.
load_dotenv(PROJECT_ROOT / ".env")


# Locate the MCP server project.
server_directory = os.getenv("MCP_SERVER_DIR", "server")

SERVER_DIR = Path(server_directory)

if not SERVER_DIR.is_absolute():
    SERVER_DIR = PROJECT_ROOT / SERVER_DIR

if not SERVER_DIR.exists():
    raise FileNotFoundError(
        f"MCP server directory not found: {SERVER_DIR}"
    )


def create_mcp_client() -> MultiServerMCPClient:
    """
    Create an MCP client that automatically launches
    the local Expense Tracker server using STDIO.
    """

    return MultiServerMCPClient(
        {
            "expense_tracker": {
                "transport": "stdio",
                "command": "uv",
                "args": [
                    "run",
                    "--project",
                    str(SERVER_DIR),
                    "python",
                    "-m",
                    "expense_server.main"
                ],
                "cwd": str(SERVER_DIR),
                "env": os.environ.copy()
            }
        }
    )


async def get_mcp_tools(client: MultiServerMCPClient):
    """Discover and return tools exposed by the MCP server."""

    return await client.get_tools()
