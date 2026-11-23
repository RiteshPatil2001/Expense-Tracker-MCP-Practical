
import json
import os
from pathlib import Path


def get_categories_file_path() -> Path:
    """Resolve the categories JSON file path."""

    project_root = Path(__file__).resolve().parents[4]

    configured_path = os.getenv(
        "CATEGORIES_FILE_PATH",
        "server/data/categories.json"
    )

    categories_path = Path(configured_path)

    if not categories_path.is_absolute():
        categories_path = project_root / categories_path

    return categories_path


def get_categories() -> list[str]:
    """Load the allowed expense categories from JSON."""

    categories_path = get_categories_file_path()

    if not categories_path.exists():
        raise FileNotFoundError(
            f"Categories file not found: {categories_path}"
        )

    with categories_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    categories = data.get("categories")

    if not isinstance(categories, list) or not categories:
        raise ValueError("Categories JSON must contain a non-empty categories list.")

    if not all(
        isinstance(category, str) and category.strip()
        for category in categories
    ):
        raise ValueError("Every category must be a non-empty string.")

    return [category.strip() for category in categories]


def validate_category(category: str) -> str:
    """Return the canonical category if it is allowed."""

    if not isinstance(category, str) or not category.strip():
        raise ValueError("Category cannot be empty.")

    allowed_categories = get_categories()

    for allowed_category in allowed_categories:
        if category.strip().casefold() == allowed_category.casefold():
            return allowed_category

    raise ValueError(
        f"Invalid category '{category}'. "
        f"Allowed categories: {', '.join(allowed_categories)}"
    )
