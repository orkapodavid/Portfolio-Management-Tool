"""
07 - Validation Page - Demonstrates data validation.

Requirement 7: Data Validation
AG Grid Feature: valueParser + Python validation + cellEditorParams.validation (v34+)
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..data import EDITABLE_VALIDATION
from ..components import nav_bar


def validation_page() -> rx.Component:
    """Validation demo page.

    Features:
    - Field-level validation rules (Python-based via validation_schema)
    - Multiple validation types (string, number, integer, enum)
    - Pattern matching for strings
    - Min/max constraints for numbers
    - Note: AG Grid v34+ also supports cellEditorParams.validation for number editors
    """
    validation_columns = [
        {"field": "symbol", "headerName": "Symbol", "editable": True, "width": 100},
        {
            "field": "price",
            "headerName": "Price ($)",
            "editable": True,
            "type": "numericColumn",
            "width": 120,
        },
        {
            "field": "qty",
            "headerName": "Quantity",
            "editable": True,
            "type": "numericColumn",
            "width": 100,
        },
        {
            "field": "change",
            "headerName": "Change (%)",
            "editable": True,
            "type": "numericColumn",
            "width": 120,
        },
        {
            "field": "sector",
            "headerName": "Sector",
            "editable": True,
            "cellEditor": "agSelectCellEditor",
            "cellEditorParams": {
                "values": ["Technology", "Finance", "Healthcare", "Energy"]
            },
            "width": 130,
        },
    ]

    return rx.vstack(
        nav_bar(),
        rx.heading("07 - Validation", size="6"),
        rx.text("Requirement 7: Data Validation"),
        rx.callout(
            "Double-click a cell to edit. Try entering invalid values to see validation.",
            icon="info",
        ),
        rx.box(
            rx.heading("Validation Rules:", size="4"),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Field"),
                        rx.table.column_header_cell("Type"),
                        rx.table.column_header_cell("Constraints"),
                    ),
                ),
                rx.table.body(
                    rx.table.row(
                        rx.table.cell("symbol"),
                        rx.table.cell("string"),
                        rx.table.cell("A-Z, 1-5 chars"),
                    ),
                    rx.table.row(
                        rx.table.cell("price"),
                        rx.table.cell("number"),
                        rx.table.cell("0 - 1,000,000"),
                    ),
                    rx.table.row(
                        rx.table.cell("qty"),
                        rx.table.cell("integer"),
                        rx.table.cell("1 - 10,000"),
                    ),
                    rx.table.row(
                        rx.table.cell("change"),
                        rx.table.cell("number"),
                        rx.table.cell("-100 to 100"),
                    ),
                    rx.table.row(
                        rx.table.cell("sector"),
                        rx.table.cell("enum"),
                        rx.table.cell("4 values"),
                    ),
                ),
            ),
            padding="3",
            background="var(--gray-2)",
            border_radius="8px",
            margin_bottom="3",
        ),
        ag_grid(
            id="validation_grid",
            row_data=DemoState.data,
            column_defs=validation_columns,
            validation_schema=EDITABLE_VALIDATION.to_js_config(),
            on_cell_value_changed=DemoState.on_cell_edit,
            theme="quartz",
            width="90vw",
            height="50vh",
        ),
        padding="4",
        spacing="3",
    )
