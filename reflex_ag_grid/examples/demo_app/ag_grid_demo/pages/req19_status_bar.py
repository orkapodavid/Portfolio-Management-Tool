"""
19 - Status Bar Page - Demonstrates status bar with aggregations.

Requirement 19: Status Bar with Live Aggregations
AG Grid Feature: statusBar + aggregation
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_basic_columns
from ..components import nav_bar, status_badge


def status_bar_page() -> rx.Component:
    """Status Bar demo page.

    Features:
    - Status bar at bottom of grid
    - Row count display
    - Selection count
    - Custom aggregation panels
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("19 - Status Bar", size="6"),
        rx.text("Display row counts and aggregations in status bar"),
        rx.callout(
            "The status bar appears at the bottom of the grid, showing row counts, "
            "selection information, and custom aggregations. Select rows to see counts update.",
            icon="info",
        ),
        status_badge(),
        ag_grid(
            id="status_bar_grid",
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            row_id_key="id",
            row_selection="multiple",
            theme="quartz",
            width="90vw",
            height="55vh",
            status_bar={
                "statusPanels": [
                    {"statusPanel": "agTotalRowCountComponent", "align": "left"},
                    {"statusPanel": "agFilteredRowCountComponent", "align": "left"},
                    {"statusPanel": "agSelectedRowCountComponent", "align": "center"},
                    {"statusPanel": "agAggregationComponent", "align": "right"},
                ],
            },
        ),
        rx.box(
            rx.heading("Status Bar Configuration:", size="4"),
            rx.code_block(
                """ag_grid(
    status_bar={
        "statusPanels": [
            {"statusPanel": "agTotalRowCountComponent", "align": "left"},
            {"statusPanel": "agFilteredRowCountComponent", "align": "left"},  
            {"statusPanel": "agSelectedRowCountComponent", "align": "center"},
            {"statusPanel": "agAggregationComponent", "align": "right"},
        ],
    },
)""",
                language="python",
            ),
            padding="3",
            background="var(--gray-2)",
            border_radius="8px",
        ),
        padding="4",
        spacing="3",
    )
