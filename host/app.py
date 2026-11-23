
import streamlit as st

from expense_host.ui.chat import render_chat_page


st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="centered"
)


render_chat_page()
