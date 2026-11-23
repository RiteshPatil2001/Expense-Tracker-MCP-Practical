
import streamlit as st


def render_header() -> None:
    """Display the application heading."""

    st.title("💰 Expense Tracker")
    st.caption("Manage your expenses using natural language.")


def render_chat_history(messages: list[dict]) -> None:
    """Display previous messages in the chat."""

    for message in messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def render_sidebar() -> None:
    """Display sidebar controls."""

    with st.sidebar:
        st.subheader("Expense Tracker")
        st.caption("Your expense records are saved locally.")

        if st.button("Clear chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()
