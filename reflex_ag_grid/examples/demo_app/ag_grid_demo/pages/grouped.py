"""
Grouped Grid Page - Demonstrates row grouping and aggregation.

Requirements:
- Req 5: Grouping & Summary
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_grouped_columns
from ..components import nav_bar, status_badge


def grouped_page() -> rx.Component:
    """Grouped Grid page with aggregation.

    Features:
    - Row grouping by sector
    - Aggregation functions (sum, avg)
    - Expandable/collapsible group rows
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("Grouped Grid", size="6"),
        rx.text("Features: Row grouping by sector, Aggregation (sum, avg)"),
        status_badge(),
        ag_grid(
            id="grouped_grid",
            row_data=DemoState.data,
            column_defs=get_grouped_columns(),
            group_default_expanded=-1,
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        padding="4",
        spacing="3",
    )
