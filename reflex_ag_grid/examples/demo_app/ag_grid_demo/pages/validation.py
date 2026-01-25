"""
Validation Demo Page - Demonstrates Phase 2 validation system.

Requirements:
- Req 7: Data Validation (.ini)
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..data import EDITABLE_VALIDATION
from ..components import nav_bar


def validation_page() -> rx.Component:
    """Validation Demo page showing Pydantic-based validation.

    Features:
    - Field-level validation rules
    - Multiple validation types (string, number, integer, enum)
    - Pattern matching for strings
    - Min/max constraints for numbers
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
        rx.heading("Validation Demo", size="6"),
        rx.text("Phase 2 Feature: Field-level validation with Pydantic models"),
        # Validation Rules Section
        rx.box(
            rx.heading("Validation Rules Applied:", size="4"),
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
                        rx.table.cell("Pattern: A-Z only, 1-5 chars, required"),
                    ),
                    rx.table.row(
                        rx.table.cell("price"),
                        rx.table.cell("number"),
                        rx.table.cell("Min: 0, Max: 1,000,000, required"),
                    ),
                    rx.table.row(
                        rx.table.cell("qty"),
                        rx.table.cell("integer"),
                        rx.table.cell("Min: 1, Max: 10,000, required"),
                    ),
                    rx.table.row(
                        rx.table.cell("change"),
                        rx.table.cell("number"),
                        rx.table.cell("Min: -100, Max: 100"),
                    ),
                    rx.table.row(
                        rx.table.cell("sector"),
                        rx.table.cell("enum"),
                        rx.table.cell(
                            "Values: Technology, Finance, Healthcare, Energy"
                        ),
                    ),
                ),
            ),
            padding="4",
            background="var(--gray-2)",
            border_radius="8px",
            margin_bottom="4",
        ),
        # Instructions
        rx.callout(
            "Double-click a cell to edit. Try entering invalid values to see validation in action.",
            icon="info",
        ),
        # Grid with validation
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
        # Code Example
        rx.box(
            rx.heading("Usage Example:", size="4"),
            rx.code_block(
                """from reflex_ag_grid import ag_grid, FieldValidation, ValidationSchema

schema = ValidationSchema(
    fields=[
        FieldValidation(
            field_name="price",
            field_type="number",
            min_value=0,
            max_value=1_000_000,
            required=True,
        ),
    ]
)

ag_grid(
    id="my_grid",
    row_data=data,
    validation_schema=schema.to_js_config(),
)""",
                language="python",
            ),
            padding="4",
            background="var(--gray-2)",
            border_radius="8px",
        ),
        padding="4",
        spacing="3",
    )
