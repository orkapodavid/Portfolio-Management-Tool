"""
AG Grid Demo App - Testing the fixed ag_grid component.

Uses the fixed ag_grid component with direct npm imports pattern.
"""

import sys
from pathlib import Path

import reflex as rx

# Add reflex_ag_grid package to path (parent of 'examples' directory)
_package_root = (
    Path(__file__).resolve().parents[3]
)  # demo_app/ag_grid_demo → reflex_ag_grid
if str(_package_root.parent) not in sys.path:
    sys.path.insert(0, str(_package_root.parent))

from reflex_ag_grid import ag_grid, ColumnDef  # noqa: E402


# =============================================================================
# SAMPLE DATA
# =============================================================================

SAMPLE_DATA = [
    {
        "id": "1",
        "symbol": "AAPL",
        "company": "Apple Inc.",
        "sector": "Technology",
        "price": 175.50,
        "qty": 100,
        "change": 2.5,
    },
    {
        "id": "2",
        "symbol": "GOOGL",
        "company": "Alphabet Inc.",
        "sector": "Technology",
        "price": 140.25,
        "qty": 50,
        "change": -1.2,
    },
    {
        "id": "3",
        "symbol": "MSFT",
        "company": "Microsoft Corp.",
        "sector": "Technology",
        "price": 378.90,
        "qty": 75,
        "change": 0.8,
    },
    {
        "id": "4",
        "symbol": "JPM",
        "company": "JPMorgan Chase",
        "sector": "Finance",
        "price": 195.00,
        "qty": 200,
        "change": 1.5,
    },
    {
        "id": "5",
        "symbol": "GS",
        "company": "Goldman Sachs",
        "sector": "Finance",
        "price": 385.75,
        "qty": 30,
        "change": -0.5,
    },
    {
        "id": "6",
        "symbol": "JNJ",
        "company": "Johnson & Johnson",
        "sector": "Healthcare",
        "price": 155.30,
        "qty": 120,
        "change": 0.3,
    },
    {
        "id": "7",
        "symbol": "PFE",
        "company": "Pfizer Inc.",
        "sector": "Healthcare",
        "price": 28.50,
        "qty": 500,
        "change": -2.1,
    },
    {
        "id": "8",
        "symbol": "XOM",
        "company": "Exxon Mobil",
        "sector": "Energy",
        "price": 105.20,
        "qty": 150,
        "change": 3.2,
    },
]


# =============================================================================
# COLUMN DEFINITIONS - Using ColumnDef Pydantic model
# =============================================================================

COLUMN_DEFS = [
    ag_grid.column_def(
        field="symbol", header_name="Symbol", sortable=True, filter="agTextColumnFilter"
    ),
    ag_grid.column_def(field="company", header_name="Company", flex=1),
    ag_grid.column_def(
        field="sector", header_name="Sector", filter="agSetColumnFilter"
    ),
    ag_grid.column_def(
        field="price", header_name="Price", sortable=True, filter="agNumberColumnFilter"
    ),
    ag_grid.column_def(field="qty", header_name="Quantity", sortable=True),
    ag_grid.column_def(field="change", header_name="Change %", sortable=True),
]


# =============================================================================
# STATE
# =============================================================================


class DemoState(rx.State):
    """Demo application state."""

    data: list[dict] = SAMPLE_DATA
    selected_rows: list[dict] = []
    last_event: str = "None"

    def on_selection_change(self, rows: list, source: str, event_type: str):
        """Handle row selection changes."""
        self.selected_rows = rows if isinstance(rows, list) else []
        self.last_event = f"Selection: {len(self.selected_rows)} rows ({source})"

    def on_cell_click(self, event: dict):
        """Handle cell clicks."""
        row_index = event.get("rowIndex", "?")
        field = event.get("colDef", {}).get("field", "?")
        self.last_event = f"Cell click: row {row_index}, field {field}"

    def on_cell_edit(self, row_index: int, field: str, new_value: str):
        """Handle cell value changes."""
        self.last_event = f"Cell edit: row {row_index}, {field} = {new_value}"


# =============================================================================
# UI COMPONENTS
# =============================================================================


def selected_row_card(row: dict) -> rx.Component:
    """Display a selected row as a card."""
    return rx.card(
        rx.data_list.root(
            rx.data_list.item(
                rx.data_list.label("Symbol"),
                rx.data_list.value(row["symbol"]),
            ),
            rx.data_list.item(
                rx.data_list.label("Company"),
                rx.data_list.value(row["company"]),
            ),
            rx.data_list.item(
                rx.data_list.label("Price"),
                rx.data_list.value(row["price"]),
            ),
        ),
        width="200px",
    )


def index() -> rx.Component:
    """Main page with AG Grid demo using the fixed component."""
    return rx.vstack(
        rx.heading("AG Grid Demo - Fixed Implementation", size="7"),
        rx.text("Using direct npm imports pattern (ag-grid-react@32.1.0)."),
        rx.badge(DemoState.last_event, color_scheme="blue"),
        # AG Grid component using the fixed implementation
        ag_grid(
            id="demo_grid",
            row_data=DemoState.data,
            column_defs=COLUMN_DEFS,
            row_selection="multiple",
            on_selection_changed=DemoState.on_selection_change,
            on_cell_clicked=DemoState.on_cell_click,
            on_cell_value_changed=DemoState.on_cell_edit,
            theme="quartz",
            width="80vw",
            height="50vh",
        ),
        # Selected rows display
        rx.cond(
            DemoState.selected_rows.length() > 0,
            rx.vstack(
                rx.heading("Selected Rows", size="5"),
                rx.hstack(
                    rx.foreach(DemoState.selected_rows, selected_row_card),
                    wrap="wrap",
                    spacing="2",
                ),
                width="100%",
            ),
            rx.text("No rows selected", color="gray"),
        ),
        padding="4",
        spacing="4",
        width="100%",
        max_width="1200px",
        margin="0 auto",
    )


# =============================================================================
# APP
# =============================================================================

app = rx.App()
app.add_page(index)
