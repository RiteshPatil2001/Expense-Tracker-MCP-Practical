
import asyncio

import streamlit as st

from expense_host.chat_manager import (
    initialize_chat,
    process_message
)
from expense_host.ui.components import (
    render_header,
    render_chat_history,
    render_sidebar
)


def render_chat_page() -> None:
    """Render and manage the Expense Tracker chat interface."""

    # Initialize session state.
    initialize_chat()

    # Render application layout.
    render_sidebar()
    render_header()

    # Display previous conversation.
    render_chat_history(st.session_state.messages)

    # Accept a new user message.
    prompt = st.chat_input("Ask me about your expenses...")

    if prompt:
        success = False

        with st.spinner("Processing your request..."):
            try:
                asyncio.run(process_message(prompt))
                success = True

            except Exception as error:
                st.error(f"Unable to process your request: {error}")

        # Refresh the page to display the updated conversation.
        if success:
            st.rerun()
