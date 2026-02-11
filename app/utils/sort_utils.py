"""
Shared Sorting Utilities

Provides a reusable sort-key function for financial data strings.
Extracted to eliminate copy-paste duplication across state mixins.
"""


def financial_sort_key(value):
    """Parse a financial string to a sortable value.

    Handles formats like:
    - "$1,234.56" → 1234.56
    - "($456.78)" → -456.78
    - "-$123.00" → -123.0
    - "1.5%" → 1.5
    - "AAPL" → "aapl" (fallback to lowercase string)

    Args:
        value: The cell value (str, int, float, etc.)

    Returns:
        A float if parseable, otherwise lowercase string for alphabetic sort.
    """
    if isinstance(value, str):
        cleaned = (
            value.replace("$", "")
            .replace(",", "")
            .replace("(", "-")
            .replace(")", "")
            .replace("%", "")
        )
        try:
            return float(cleaned)
        except ValueError:
            return value.lower()
    return value
