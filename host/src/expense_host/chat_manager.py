
import streamlit as st

from expense_host.client import create_mcp_client, get_mcp_tools
from expense_host.agent import create_expense_agent


def initialize_chat() -> None:
    """
    Initialize chat state for the current Streamlit session.
    """

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "expense_agent" not in st.session_state:
        st.session_state.expense_agent = None


async def get_agent():
    """
    Create the MCP client and expense agent when needed.
    """

    if st.session_state.expense_agent is None:
        client = create_mcp_client()

        tools = await get_mcp_tools(client)

        st.session_state.expense_agent = create_expense_agent(tools)

    return st.session_state.expense_agent


async def process_message(user_message: str) -> str:
    """
    Process a user message through the Groq expense agent.
    """

    user_message = user_message.strip()

    if not user_message:
        return "Please enter a message."

    initialize_chat()

    # Add the user's message to session-only history.
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_message
        }
    )

    try:
        agent = await get_agent()

        # Pass the current conversation to the agent.
        response = await agent.ainvoke(
            {
                "messages": st.session_state.messages
            }
        )

        # Extract the latest assistant response.
        assistant_message = response["messages"][-1]
        assistant_content = assistant_message.content

        if isinstance(assistant_content, list):
            assistant_content = "\n".join(
                str(item.get("text", item))
                if isinstance(item, dict)
                else str(item)
                for item in assistant_content
            )

        if not isinstance(assistant_content, str):
            assistant_content = str(assistant_content)

        # Store only the final assistant response.
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_content
            }
        )

        return assistant_content

    except Exception:
        # Remove the unanswered user message so it isn't
        # included in the next request as an incomplete turn.
        st.session_state.messages.pop()

        raise
