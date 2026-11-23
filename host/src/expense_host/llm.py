
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq


# Locate the repository root and load its .env file.
PROJECT_ROOT = Path(__file__).resolve().parents[3]

load_dotenv(PROJECT_ROOT / ".env")


def get_llm() -> ChatGroq:
    """Create and return the configured Groq chat model."""

    api_key = os.getenv("GROQ_API_KEY")
    model = os.getenv("GROQ_MODEL")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Add it to the root .env file."
        )

    if not model:
        raise ValueError(
            "GROQ_MODEL is missing. Add your Groq model name to .env."
        )

    return ChatGroq(
        model=model,
        api_key=api_key,
        temperature=0
    )
