"""
26 - Quick Filter Page - Demonstrates AG Grid Quick Filter text search.

Requirement 26: Quick Filter Search
AG Grid Feature: quickFilterText, quickFilterParser
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_basic_columns
from ..components import nav_bar


class QuickFilterState(rx.State):
    """State for Quick Filter demo page."""

    search_text: str = ""

    def set_search(self, value: str):
        """Set the search text."""
        self.search_text = value

    def clear_search(self):
        """Clear the search text."""
        self.search_text = ""


def quick_filter_page() -> rx.Component:
    """Quick Filter demo page.

    Features:
    - Text input for instant search across all columns
    - Clear button to reset the filter
    - AG Grid with quickFilterText prop
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("26 - Quick Filter Search", size="6"),
        rx.text("Requirement 26: AG Grid Quick Filter text search"),
        rx.callout(
            "Type in the search box to instantly filter all columns. "
            "Quick Filter searches across all visible columns.",
            icon="search",
        ),
        rx.hstack(
            rx.text("Search:", weight="bold"),
            rx.input(
                placeholder="Type to search...",
                value=QuickFilterState.search_text,
                on_change=QuickFilterState.set_search,
                width="300px",
            ),
            rx.button(
                "Clear",
                on_click=QuickFilterState.clear_search,
                color_scheme="gray",
            ),
            spacing="3",
            align="center",
        ),
        ag_grid(
            id="quick_filter_grid",
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            row_id_key="id",
            quick_filter_text=QuickFilterState.search_text,
            theme="quartz",
            width="90vw",
            height="55vh",
        ),
        rx.text(
            "The quickFilterText prop filters data across all columns instantly. "
            "This is a Community feature (no Enterprise license required).",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
