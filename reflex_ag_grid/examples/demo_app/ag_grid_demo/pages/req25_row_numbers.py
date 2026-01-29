"""
25 - Row Numbers Page - Demonstrates AG Grid Row Numbers feature.

Requirement 25: Row Numbers (v33.1+)
AG Grid Feature: rowNumbers: true | RowNumbersOptions
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_basic_columns
from ..components import nav_bar


def row_numbers_page() -> rx.Component:
    """Row Numbers demo page.

    Features:
    - Automatic row numbering
    - Numbers update with sort/filter
    - Works with grouping
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("25 - Row Numbers", size="6"),
        rx.text("Requirement 25: AG Grid Row Numbers"),
        rx.callout(
            "The first column shows automatic row numbers. "
            "Try sorting or filtering - numbers update automatically.",
            icon="info",
        ),
        ag_grid(
            id="row_numbers_grid",
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            row_id_key="id",
            row_numbers=True,
            theme="quartz",
            width="90vw",
            height="55vh",
        ),
        rx.text(
            "Feature: rowNumbers=True adds an automatic row number column.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
