"""
Range Selection Page - Demonstrates bulk range selection.

Requirements:
- Req 2: Bulk state changes (Range)
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_basic_columns
from ..components import nav_bar, status_badge


def range_page() -> rx.Component:
    """Range Selection page for bulk updates.

    Features:
    - Multi-cell range selection
    - Shift+click to select range
    - Multiple row selection
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("Range Selection", size="6"),
        rx.text("Features: Multi-cell selection (Shift+click), Bulk updates"),
        status_badge(),
        ag_grid(
            id="range_grid",
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            enable_range_selection=True,
            row_selection="multiple",
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        rx.text("Hold Shift and drag to select a range of cells", color="gray"),
        padding="4",
        spacing="3",
    )
