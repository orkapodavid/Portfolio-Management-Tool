"""
24 - Multi Filter Page - Demonstrates the AG Grid Enterprise Multi Filter.

Requirement 24: Multi Filter (Enterprise)
AG Grid Feature: filter: 'agMultiColumnFilter'
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..components import nav_bar


def multi_filter_page() -> rx.Component:
    """Multi Filter demo page.

    Features:
    - Combined filter with multiple filter types
    - Text filter + Set filter in one column
    - Flexible filter composition
    """
    # Define columns with Multi Filter
    multi_filter_columns = [
        {"field": "id", "headerName": "ID", "width": 80},
        {
            "field": "symbol",
            "headerName": "Symbol",
            "filter": "agMultiColumnFilter",
            "filterParams": {
                "filters": [
                    {
                        "filter": "agTextColumnFilter",
                        "display": "accordion",
                        "title": "Text Filter",
                    },
                    {
                        "filter": "agSetColumnFilter",
                        "display": "accordion",
                        "title": "Set Filter",
                    },
                ],
            },
            "width": 120,
        },
        {
            "field": "sector",
            "headerName": "Sector",
            "filter": "agMultiColumnFilter",
            "filterParams": {
                "filters": [
                    {
                        "filter": "agTextColumnFilter",
                        "display": "accordion",
                        "title": "Text Filter",
                        "filterParams": {"buttons": ["reset"]},
                    },
                    {
                        "filter": "agSetColumnFilter",
                        "display": "accordion",
                        "title": "Set Filter",
                    },
                ],
            },
            "width": 150,
        },
        {
            "field": "price",
            "headerName": "Price",
            "type": "numericColumn",
            "filter": "agMultiColumnFilter",
            "filterParams": {
                "filters": [
                    {
                        "filter": "agNumberColumnFilter",
                        "display": "accordion",
                        "title": "Number Filter",
                    },
                    {
                        "filter": "agSetColumnFilter",
                        "display": "accordion",
                        "title": "Set Filter",
                    },
                ],
            },
            "width": 120,
        },
        {"field": "qty", "headerName": "Qty", "type": "numericColumn", "width": 100},
        {
            "field": "change",
            "headerName": "Change %",
            "type": "numericColumn",
            "width": 100,
        },
    ]

    return rx.vstack(
        nav_bar(),
        rx.heading("24 - Multi Filter", size="6"),
        rx.text("Requirement 24: AG Grid Enterprise Multi Filter"),
        rx.callout(
            "Click the filter icon in Symbol, Sector, or Price columns. "
            "Expand the accordion sections to switch between filter types.",
            icon="info",
        ),
        ag_grid(
            id="multi_filter_grid",
            row_data=DemoState.data,
            column_defs=multi_filter_columns,
            row_id_key="id",
            theme="quartz",
            width="90vw",
            height="55vh",
        ),
        rx.text(
            "Enterprise feature: filter='agMultiColumnFilter' combines multiple filter types.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
