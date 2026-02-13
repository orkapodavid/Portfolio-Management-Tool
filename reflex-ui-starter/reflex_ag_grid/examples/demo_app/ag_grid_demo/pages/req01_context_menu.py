"""
01 - Context Menu Page - Demonstrates right-click context menu.

Requirement 1: Right-click context menu
AG Grid Feature: getContextMenuItems()
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_basic_columns
from ..components import nav_bar, status_badge


def context_menu_page() -> rx.Component:
    """Context Menu demo page.

    Features:
    - Right-click on any cell to see context menu
    - Copy cell value
    - Copy with headers
    - Export options in menu
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("01 - Context Menu", size="6"),
        rx.text("Requirement 1: Right-click context menu"),
        rx.callout(
            "Right-click on any cell to see the context menu with copy and export options.",
            icon="info",
        ),
        status_badge(),
        ag_grid(
            id="context_menu_grid",
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            row_selection="multiple",
            on_selection_changed=DemoState.on_selection_change,
            on_cell_clicked=DemoState.on_cell_click,
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        rx.text(
            "AG Grid Enterprise provides built-in context menu. "
            "Community edition shows browser default menu.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
