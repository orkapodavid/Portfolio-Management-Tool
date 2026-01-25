"""
05 - Grouping & Summary Page - Demonstrates row grouping and aggregation.

Requirement 5: Grouping & Summary
AG Grid Feature: rowGroup + aggFunc
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_grouped_columns
from ..components import nav_bar, status_badge


def grouping_page() -> rx.Component:
    """Grouping & Summary page.

    Features:
    - Row grouping by sector column
    - Aggregation functions (sum, avg)
    - Expandable/collapsible group rows
    - Group summaries with totals
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("05 - Grouping & Summary", size="6"),
        rx.text("Requirement 5: Grouping & Summary"),
        rx.callout(
            "Rows are grouped by Sector. Click group rows to expand/collapse. "
            "Summary shows aggregated values (avg price, sum quantity).",
            icon="info",
        ),
        status_badge(),
        ag_grid(
            id="grouping_grid",
            row_data=DemoState.data,
            column_defs=get_grouped_columns(),
            group_default_expanded=-1,  # -1 = all expanded
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        rx.text(
            "Enterprise feature: Row grouping with aggregation functions.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
