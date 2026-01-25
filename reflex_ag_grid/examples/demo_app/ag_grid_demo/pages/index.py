"""
Basic Grid Page - Demonstrates context menu, copy, and export.

Requirements:
- Req 1: Right-click context menu
- Req 8: Copy cell/with header
- Req 9: Export Excel/CSV
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_basic_columns
from ..components import nav_bar, status_badge


def index() -> rx.Component:
    """Basic Grid page with export functionality.

    Features:
    - Multiple row selection
    - Context menu (right-click)
    - Export to Excel/CSV
    - Sorting and filtering
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("Basic Grid", size="6"),
        rx.text("Features: Context menu (right-click), Copy, Export"),
        status_badge(),
        ag_grid(
            id="basic_grid",
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            row_selection="multiple",
            on_selection_changed=DemoState.on_selection_change,
            on_cell_clicked=DemoState.on_cell_click,
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        rx.hstack(
            rx.button(
                "Export Excel",
                on_click=rx.call_script("window.gridApi?.exportDataAsExcel()"),
            ),
            rx.button(
                "Export CSV",
                on_click=rx.call_script("window.gridApi?.exportDataAsCsv()"),
            ),
        ),
        padding="4",
        spacing="3",
    )
