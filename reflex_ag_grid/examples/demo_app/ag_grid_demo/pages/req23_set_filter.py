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
    # Define columns with Set Filter and other filter types
    set_filter_columns = [
        {
            "field": "id", 
            "headerName": "ID", 
            "width": 80,
            "filter": "agTextColumnFilter",
        },
        {
            "field": "symbol", 
            "headerName": "Symbol", 
            "width": 100,
            "filter": "agTextColumnFilter",
        },
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
            "field": "status",
            "headerName": "Status",
            "filter": "agSetColumnFilter",
            "width": 100,
        },
        {
            "field": "price",
            "headerName": "Price",
            "type": "numericColumn",
            "width": 120,
            "filter": "agNumberColumnFilter",
        },
        {
            "field": "qty", 
            "headerName": "Qty", 
            "type": "numericColumn", 
            "width": 100,
            "filter": "agNumberColumnFilter",
        },
    ]

    return rx.vstack(
        nav_bar(),
        rx.heading("23 - Set Filter", size="6"),
        rx.text("Requirement 23: AG Grid Enterprise Set Filter"),
        rx.callout(
            "Use the checkboxes on the left for row selection. "
            "Click the filter icon in headers to filter data (Set Filter available for Sector/Status).",
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
            auto_size_strategy={"type": "fitCellContents"},
        ),
        rx.text(
            "Enterprise feature: filter='agSetColumnFilter' enables multi-select checkbox filtering.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
