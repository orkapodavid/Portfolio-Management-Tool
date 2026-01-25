"""
Search Page - Demonstrates global quick filter search.
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_basic_columns
from ..components import nav_bar


def search_page() -> rx.Component:
    """Search/Quick Filter page.

    Features:
    - Filter all columns with single text input
    - Real-time filtering as you type
    - Clear button to reset filter
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("Global Search / Quick Filter", size="6"),
        rx.text("Features: Filter all columns with a single text input"),
        rx.hstack(
            rx.input(
                placeholder="🔍 Search all columns...",
                value=DemoState.search_text,
                on_change=DemoState.set_search_text,
                width="400px",
            ),
            rx.button("Clear", on_click=DemoState.set_search_text(""), size="2"),
            rx.text("Filtering by: ", color="gray"),
            rx.cond(
                DemoState.search_text != "",
                rx.badge(DemoState.search_text, color_scheme="blue"),
                rx.text("(none)", color="gray"),
            ),
            spacing="3",
        ),
        ag_grid(
            id="search_grid",
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            quick_filter_text=DemoState.search_text,
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        rx.text(
            "Type to filter across Symbol, Company, Sector, Price, Quantity, and Change columns.",
            color="gray",
        ),
        padding="4",
        spacing="3",
    )
