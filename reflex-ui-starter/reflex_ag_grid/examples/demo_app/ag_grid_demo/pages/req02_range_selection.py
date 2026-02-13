"""
02 - Range Selection Page - Demonstrates bulk range selection.

Requirement 2: Bulk state changes (Range)
AG Grid Feature: cellSelection (v35 API, replaces deprecated enableRangeSelection)
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_basic_columns
from ..components import nav_bar, status_badge


def range_selection_page() -> rx.Component:
    """Range Selection page for bulk updates.

    Features:
    - Multi-cell range selection (cellSelection)
    - Shift+click to select range
    - Multiple row selection
    - Drag to select cells
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("02 - Range Selection", size="6"),
        rx.text("Requirement 2: Bulk state changes (Range)"),
        rx.callout(
            "Click and drag to select a range of cells. "
            "Use Shift+Click to extend selection.",
            icon="info",
        ),
        status_badge(),
        ag_grid(
            id="range_selection_grid",
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            cell_selection=True,  # v35 API (replaces deprecated enableRangeSelection)
            row_selection="multiple",
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        rx.text(
            "Range selection is an Enterprise feature. "
            "Apply bulk updates to selected cells.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
