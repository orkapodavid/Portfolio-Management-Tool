"""
11 - Cell Editors Page - Demonstrates different cell editors.

Requirement 11: Different Cell Editors
AG Grid Feature: cellEditor mapping
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..data import SECTORS
from ..components import nav_bar, status_badge


def cell_editors_page() -> rx.Component:
    """Cell Editors demo page.

    Features:
    - Text editor (default)
    - Number editor
    - Select/dropdown editor
    - Checkbox editor
    - Date editor
    """
    editor_columns = [
        {
            "field": "symbol",
            "headerName": "Symbol (Text)",
            "editable": False,
            "width": 120,
        },
        {
            "field": "company",
            "headerName": "Company (Text)",
            "editable": True,
            "width": 150,
        },
        {
            "field": "sector",
            "headerName": "Sector (Select)",
            "editable": True,
            "cellEditor": "agSelectCellEditor",
            "cellEditorParams": {"values": SECTORS},
            "width": 130,
        },
        {
            "field": "price",
            "headerName": "Price (Number)",
            "editable": True,
            "cellEditor": "agNumberCellEditor",
            "width": 120,
        },
        {
            "field": "qty",
            "headerName": "Qty (Large Text)",
            "editable": True,
            "cellEditor": "agLargeTextCellEditor",
            "cellEditorPopup": True,
            "width": 120,
        },
        {
            "field": "active",
            "headerName": "Active (Check)",
            "editable": True,
            "cellEditor": "agCheckboxCellEditor",
            "cellRenderer": "agCheckboxCellRenderer",
            "width": 100,
        },
    ]

    return rx.vstack(
        nav_bar(),
        rx.heading("11 - Cell Editors", size="6"),
        rx.text("Requirement 11: Different Cell Editors"),
        rx.callout(
            "Double-click cells to see different editor types.",
            icon="info",
        ),
        rx.box(
            rx.heading("Editor Types:", size="4"),
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.column_header_cell("Column"),
                        rx.table.column_header_cell("Editor Type"),
                    ),
                ),
                rx.table.body(
                    rx.table.row(
                        rx.table.cell("Company"), rx.table.cell("Text (default)")
                    ),
                    rx.table.row(
                        rx.table.cell("Sector"), rx.table.cell("Select dropdown")
                    ),
                    rx.table.row(rx.table.cell("Price"), rx.table.cell("Number")),
                    rx.table.row(
                        rx.table.cell("Qty"), rx.table.cell("Large text popup")
                    ),
                    rx.table.row(rx.table.cell("Active"), rx.table.cell("Checkbox")),
                ),
            ),
            padding="3",
            background="var(--gray-2)",
            border_radius="8px",
            margin_bottom="3",
        ),
        status_badge(),
        ag_grid(
            id="cell_editors_grid",
            row_data=DemoState.data,
            column_defs=editor_columns,
            on_cell_value_changed=DemoState.on_cell_edit,
            on_cell_editing_started=DemoState.on_editing_started,
            on_cell_editing_stopped=DemoState.on_editing_stopped,
            theme="quartz",
            width="90vw",
            height="55vh",
        ),
        padding="4",
        spacing="3",
    )
