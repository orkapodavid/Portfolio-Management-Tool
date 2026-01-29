"""
23 - Set Filter Page - Demonstrates the AG Grid Enterprise Set Filter.

Requirement 23: Set Filter (Enterprise)
AG Grid Feature: filter: 'agSetColumnFilter'
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..components import nav_bar


def set_filter_page() -> rx.Component:
    """Set Filter demo page.

    Features:
    - Multi-select checkbox filter
    - Search within filter values
    - Select All / Deselect All
    """
    # Define columns with Set Filter
    set_filter_columns = [
        {"field": "id", "headerName": "ID", "width": 80},
        {"field": "symbol", "headerName": "Symbol", "width": 100},
        {
            "field": "sector",
            "headerName": "Sector",
            "filter": "agSetColumnFilter",
            "filterParams": {
                "buttons": ["reset", "apply"],
            },
            "width": 150,
        },
        {
            "field": "currency",
            "headerName": "Currency",
            "filter": "agSetColumnFilter",
            "width": 100,
        },
        {
            "field": "price",
            "headerName": "Price",
            "type": "numericColumn",
            "width": 120,
        },
        {"field": "qty", "headerName": "Qty", "type": "numericColumn", "width": 100},
    ]

    return rx.vstack(
        nav_bar(),
        rx.heading("23 - Set Filter", size="6"),
        rx.text("Requirement 23: AG Grid Enterprise Set Filter"),
        rx.callout(
            "Click the filter icon in Sector or Currency columns to see the Set Filter. "
            "Use checkboxes to select multiple values.",
            icon="info",
        ),
        ag_grid(
            id="set_filter_grid",
            row_data=DemoState.data,
            column_defs=set_filter_columns,
            row_id_key="id",
            side_bar="filters",  # Show filters sidebar
            theme="quartz",
            width="90vw",
            height="55vh",
        ),
        rx.text(
            "Enterprise feature: filter='agSetColumnFilter' enables multi-select checkbox filtering.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
