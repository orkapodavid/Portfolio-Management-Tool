"""
08 - Clipboard Page - Demonstrates copy cell with/without header.

Requirement 8: Copy cell / with header
AG Grid Feature: Clipboard API
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_basic_columns
from ..components import nav_bar, status_badge


def clipboard_page() -> rx.Component:
    """Clipboard demo page.

    Features:
    - Copy cell value (Ctrl+C)
    - Copy with headers
    - Paste values (Ctrl+V)
    - Context menu copy options
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("08 - Clipboard", size="6"),
        rx.text("Requirement 8: Copy cell / with header"),
        rx.callout(
            "Select cells and use Ctrl+C to copy. Right-click for copy options.",
            icon="info",
        ),
        rx.hstack(
            rx.text("Keyboard shortcuts:", weight="bold"),
            rx.badge("Ctrl+C", color_scheme="blue"),
            rx.text("Copy cells"),
            rx.badge("Ctrl+V", color_scheme="green"),
            rx.text("Paste"),
            spacing="2",
        ),
        status_badge(),
        ag_grid(
            id="clipboard_grid",
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            row_selection="multiple",
            enable_range_selection=True,
            on_selection_changed=DemoState.on_selection_change,
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        rx.text(
            "Enterprise feature: Copy with headers, paste from Excel.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
