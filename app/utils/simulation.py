"""
Simulation Utilities — Demo data fluctuation logic.

Contains the business/data logic for simulating live market data updates.
Extracted from state mixins to keep the UI layer free of data manipulation.
"""

import random
from typing import Any


def simulate_financial_tick(
    rows: list[dict[str, Any]],
    value_fields: list[str],
    pct_fields: list[str] | None = None,
    num_rows: int = 5,
    value_jitter: tuple[float, float] = (0.95, 1.05),
    pct_jitter: tuple[float, float] = (0.9, 1.1),
) -> list[dict[str, Any]]:
    """Apply random fluctuations to a list of financial data rows.

    Creates new row dicts (immutable update) for AG Grid change detection.

    Args:
        rows: List of data row dicts.
        value_fields: Field names containing dollar-formatted values
                      (e.g. "$1,234", "($456)", "-$123").
        pct_fields: Optional field names containing percentage values
                    (e.g. "+1.5%", "-0.3%").
        num_rows: Max number of rows to update per tick.
        value_jitter: (min, max) multiplier range for value fluctuation.
        pct_jitter: (min, max) multiplier range for percentage fluctuation.

    Returns:
        New list with updated rows (unchanged rows are same object references).
    """
    if not rows:
        return rows

    new_list = list(rows)
    count = random.randint(1, min(num_rows, len(new_list)))

    for _ in range(count):
        idx = random.randint(0, len(new_list) - 1)
        new_row = dict(new_list[idx])

        # Fluctuate dollar-formatted values
        for field in value_fields:
            if field in new_row and new_row[field]:
                new_row[field] = _jitter_dollar_value(new_row[field], value_jitter)

        # Fluctuate percentage values
        if pct_fields:
            for field in pct_fields:
                if field in new_row and new_row[field]:
                    new_row[field] = _jitter_pct_value(new_row[field], pct_jitter)

        new_list[idx] = new_row

    return new_list


def simulate_numeric_tick(
    rows: list[dict[str, Any]],
    fields: list[str],
    num_rows: int = 3,
    jitter: tuple[float, float] = (0.98, 1.02),
) -> list[dict[str, Any]]:
    """Apply random fluctuations to numeric (non-formatted) fields.

    Used for risk Greeks and other raw numeric data.

    Args:
        rows: List of data row dicts.
        fields: Field names containing raw numeric values.
        num_rows: Max number of rows to update per tick.
        jitter: (min, max) multiplier range.

    Returns:
        New list with updated rows.
    """
    if not rows:
        return rows

    new_list = list(rows)
    count = random.randint(1, min(num_rows, len(new_list)))

    for _ in range(count):
        idx = random.randint(0, len(new_list) - 1)
        new_row = dict(new_list[idx])

        for field in fields:
            if field in new_row and new_row[field] is not None:
                try:
                    val = float(new_row[field])
                    new_row[field] = round(val * random.uniform(*jitter), 4)
                except (ValueError, TypeError):
                    pass

        new_list[idx] = new_row

    return new_list


# --- Internal helpers ---


def _jitter_dollar_value(val_str: str, jitter: tuple[float, float]) -> str:
    """Apply random jitter to a dollar-formatted string."""
    try:
        raw = str(val_str)
        is_negative = "(" in raw or raw.startswith("-")
        val = float(
            raw.replace("$", "")
            .replace(",", "")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .strip()
        )
        if is_negative:
            val = -val
        new_val = round(val * random.uniform(*jitter), 2)
        if new_val < 0:
            return f"-${abs(new_val):,.2f}"
        return f"${new_val:,.2f}"
    except (ValueError, TypeError):
        return val_str


def _jitter_pct_value(val_str: str, jitter: tuple[float, float]) -> str:
    """Apply random jitter to a percentage-formatted string."""
    try:
        val = float(str(val_str).replace("%", "").replace("+", ""))
        new_val = round(val * random.uniform(*jitter), 2)
        return f"{new_val:+.1f}%"
    except (ValueError, TypeError):
        return val_str
