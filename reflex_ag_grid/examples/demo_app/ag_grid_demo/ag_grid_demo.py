"""
AG Grid Demo App - Main Application

Multi-page Reflex app demonstrating all AG Grid Enterprise features:
- Basic Grid: Simple data display
- Editable Grid: Cell editing with validation
- Grouped Grid: Row grouping with aggregation
- Streaming Data: Mock real-time updates
"""

import random
import sys
from pathlib import Path

import reflex as rx

# Add the project root to path so reflex_ag_grid can be imported
# demo_app is at: reflex_ag_grid/examples/demo_app/ag_grid_demo/
# We need to go up 4 levels to get to the project root
_project_root = Path(__file__).parent.parent.parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from reflex_ag_grid import AGGrid, ColumnDef, ColumnType  # noqa: E402


# =============================================================================
# SAMPLE DATA
# =============================================================================

SAMPLE_STOCKS = [
    {
        "id": "1",
        "symbol": "AAPL",
        "name": "Apple Inc.",
        "sector": "Technology",
        "price": 178.50,
        "quantity": 100,
        "change": 2.35,
    },
    {
        "id": "2",
        "symbol": "GOOGL",
        "name": "Alphabet Inc.",
        "sector": "Technology",
        "price": 141.25,
        "quantity": 50,
        "change": -1.20,
    },
    {
        "id": "3",
        "symbol": "MSFT",
        "name": "Microsoft Corp.",
        "sector": "Technology",
        "price": 378.90,
        "quantity": 75,
        "change": 0.85,
    },
    {
        "id": "4",
        "symbol": "AMZN",
        "name": "Amazon.com Inc.",
        "sector": "Consumer",
        "price": 178.25,
        "quantity": 25,
        "change": -0.50,
    },
    {
        "id": "5",
        "symbol": "TSLA",
        "name": "Tesla Inc.",
        "sector": "Automotive",
        "price": 248.50,
        "quantity": 30,
        "change": 5.75,
    },
    {
        "id": "6",
        "symbol": "NVDA",
        "name": "NVIDIA Corp.",
        "sector": "Technology",
        "price": 875.30,
        "quantity": 20,
        "change": 12.40,
    },
    {
        "id": "7",
        "symbol": "JPM",
        "name": "JPMorgan Chase",
        "sector": "Finance",
        "price": 195.80,
        "quantity": 40,
        "change": -0.25,
    },
    {
        "id": "8",
        "symbol": "V",
        "name": "Visa Inc.",
        "sector": "Finance",
        "price": 275.60,
        "quantity": 35,
        "change": 1.15,
    },
    {
        "id": "9",
        "symbol": "WMT",
        "name": "Walmart Inc.",
        "sector": "Consumer",
        "price": 165.40,
        "quantity": 60,
        "change": 0.45,
    },
    {
        "id": "10",
        "symbol": "PG",
        "name": "Procter & Gamble",
        "sector": "Consumer",
        "price": 158.20,
        "quantity": 45,
        "change": -0.80,
    },
]


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================

BASIC_COLUMNS = [
    ColumnDef(field="symbol", header_name="Symbol", width=100, pinned="left"),
    ColumnDef(field="name", header_name="Company", min_width=180, flex=1),
    ColumnDef(field="sector", header_name="Sector", width=120),
    ColumnDef(
        field="price",
        header_name="Price",
        type=ColumnType.FLOAT,
        width=120,
        formatter="currency",
    ),
    ColumnDef(
        field="quantity",
        header_name="Qty",
        type=ColumnType.INTEGER,
        width=100,
        formatter="number",
    ),
    ColumnDef(
        field="change",
        header_name="Change %",
        type=ColumnType.FLOAT,
        width=120,
        formatter="percentage_value",
        cell_class_rules="traffic_light",
    ),
]

EDITABLE_COLUMNS = [
    ColumnDef(
        field="symbol", header_name="Symbol", width=100, pinned="left", editable=False
    ),
    ColumnDef(
        field="name", header_name="Company", min_width=180, flex=1, editable=True
    ),
    ColumnDef(
        field="sector",
        header_name="Sector",
        type=ColumnType.ENUM,
        width=120,
        editable=True,
        enum_values=["Technology", "Finance", "Consumer", "Automotive", "Healthcare"],
    ),
    ColumnDef(
        field="price",
        header_name="Price",
        type=ColumnType.FLOAT,
        width=120,
        editable=True,
        formatter="currency",
        validation={"min": 0, "max": 10000},
    ),
    ColumnDef(
        field="quantity",
        header_name="Qty",
        type=ColumnType.INTEGER,
        width=100,
        editable=True,
        formatter="number",
        validation={"min": 1, "max": 10000},
    ),
    ColumnDef(
        field="change",
        header_name="Change %",
        type=ColumnType.FLOAT,
        width=120,
        formatter="percentage_value",
        cell_class_rules="traffic_light",
    ),
]

GROUPED_COLUMNS = [
    ColumnDef(field="sector", header_name="Sector", row_group=True, hide=True),
    ColumnDef(field="symbol", header_name="Symbol", width=100),
    ColumnDef(field="name", header_name="Company", min_width=180, flex=1),
    ColumnDef(
        field="price",
        header_name="Price",
        type=ColumnType.FLOAT,
        width=120,
        formatter="currency",
        agg_func="avg",
    ),
    ColumnDef(
        field="quantity",
        header_name="Qty",
        type=ColumnType.INTEGER,
        width=100,
        formatter="number",
        agg_func="sum",
    ),
    ColumnDef(
        field="change",
        header_name="Change %",
        type=ColumnType.FLOAT,
        width=120,
        formatter="percentage_value",
        cell_class_rules="traffic_light",
        agg_func="avg",
    ),
]


# =============================================================================
# STATE
# =============================================================================


class DemoState(rx.State):
    """Main state for the demo app."""

    # Data
    basic_data: list[dict] = SAMPLE_STOCKS.copy()
    editable_data: list[dict] = SAMPLE_STOCKS.copy()
    grouped_data: list[dict] = SAMPLE_STOCKS.copy()
    streaming_data: list[dict] = SAMPLE_STOCKS.copy()

    # Streaming control
    auto_refresh: bool = False
    update_count: int = 0

    # Notifications (simplified - no mixin)
    notification_messages: list[str] = []

    # Column defs (pre-serialized for reactive binding)
    @rx.var
    def basic_column_defs(self) -> list[dict]:
        return [col.to_ag_grid_def() for col in BASIC_COLUMNS]

    @rx.var
    def editable_column_defs(self) -> list[dict]:
        return [col.to_ag_grid_def() for col in EDITABLE_COLUMNS]

    @rx.var
    def grouped_column_defs(self) -> list[dict]:
        return [col.to_ag_grid_def() for col in GROUPED_COLUMNS]

    @rx.var
    def has_notifications(self) -> bool:
        return len(self.notification_messages) > 0

    # ===== Event Handlers =====

    def handle_cell_edit(self, data: dict):
        """Handle cell edit from any grid."""
        row_id = data.get("rowId", "")
        field = data.get("field", "")
        old_value = data.get("oldValue")
        new_value = data.get("newValue")

        # Update editable data
        for i, row in enumerate(self.editable_data):
            if row.get("id") == row_id:
                self.editable_data[i] = {**row, field: new_value}
                break

        # Add notification
        msg = f"✓ Updated {field}: {old_value} → {new_value}"
        self.notification_messages = [msg] + self.notification_messages[:4]

    def clear_notifications(self):
        """Clear all notifications."""
        self.notification_messages = []

    def toggle_auto_refresh(self):
        """Toggle streaming updates (manual only for 0.8.26 compatibility)."""
        self.auto_refresh = not self.auto_refresh

    def manual_refresh(self):
        """Single manual refresh - simulates price updates."""
        updated_data = []
        for row in self.streaming_data:
            new_row = row.copy()
            change = random.uniform(-2, 2)
            new_row["price"] = round(row["price"] * (1 + change / 100), 2)
            new_row["change"] = round(change, 2)
            updated_data.append(new_row)

        self.streaming_data = updated_data
        self.update_count += 1

    def reset_streaming_data(self):
        """Reset to original data."""
        self.streaming_data = SAMPLE_STOCKS.copy()
        self.update_count = 0

    # Grid control via rx.call_script
    def export_excel(self, grid_id: str):
        return rx.call_script(f"window.gridControllers?.['{grid_id}']?.exportExcel()")

    def export_csv(self, grid_id: str):
        return rx.call_script(f"window.gridControllers?.['{grid_id}']?.exportCsv()")


# =============================================================================
# COMPONENTS
# =============================================================================


def nav_bar() -> rx.Component:
    """Navigation bar."""
    return rx.hstack(
        rx.link(rx.button("Basic Grid", variant="ghost"), href="/"),
        rx.link(rx.button("Editable", variant="ghost"), href="/editable"),
        rx.link(rx.button("Grouped", variant="ghost"), href="/grouped"),
        rx.link(rx.button("Streaming", variant="ghost"), href="/streaming"),
        rx.spacer(),
        rx.text("AG Grid Demo", font_weight="bold", font_size="lg"),
        width="100%",
        padding="3",
        bg="gray.900",
        border_bottom="1px solid",
        border_color="gray.700",
    )


def notification_panel() -> rx.Component:
    """Notification panel component (simplified)."""
    return rx.cond(
        DemoState.has_notifications,
        rx.vstack(
            rx.hstack(
                rx.text("Notifications", font_weight="bold"),
                rx.spacer(),
                rx.button(
                    "Clear",
                    size="1",
                    variant="ghost",
                    on_click=DemoState.clear_notifications,
                ),
                width="100%",
            ),
            rx.foreach(
                DemoState.notification_messages,
                lambda msg: rx.box(
                    rx.text(msg, font_size="2"),
                    padding="2",
                    bg="gray.800",
                    border_radius="md",
                    width="100%",
                ),
            ),
            spacing="2",
            width="100%",
            padding="3",
            bg="gray.900",
            border_radius="md",
        ),
        rx.box(),
    )


def toolbar(grid_id: str, show_export: bool = True) -> rx.Component:
    """Standard toolbar."""
    buttons = []
    if show_export:
        buttons.extend(
            [
                rx.button(
                    rx.icon("file-spreadsheet", size=16),
                    "Excel",
                    on_click=lambda: DemoState.export_excel(grid_id),
                    variant="outline",
                    size="2",
                ),
                rx.button(
                    rx.icon("file-text", size=16),
                    "CSV",
                    on_click=lambda: DemoState.export_csv(grid_id),
                    variant="outline",
                    size="2",
                ),
            ]
        )

    return rx.hstack(
        *buttons,
        spacing="2",
        padding="2",
    )


# =============================================================================
# PAGES
# =============================================================================


def basic_page() -> rx.Component:
    """Basic grid page - simple data display."""
    return rx.box(
        nav_bar(),
        rx.vstack(
            rx.heading("Basic Grid", size="5"),
            rx.text(
                "Simple data display with sorting, filtering, and export.",
                color="gray.400",
            ),
            toolbar("basic_grid"),
            AGGrid.create(
                column_defs=DemoState.basic_column_defs,
                row_data=DemoState.basic_data,
                grid_id="basic_grid",
                theme="ag-theme-balham-dark",
                height="500px",
                width="100%",
            ),
            spacing="4",
            padding="4",
            width="100%",
        ),
        bg="gray.950",
        min_height="100vh",
    )


def editable_page() -> rx.Component:
    """Editable grid page - cell editing with validation."""
    return rx.box(
        nav_bar(),
        rx.vstack(
            rx.heading("Editable Grid", size="5"),
            rx.text(
                "Double-click cells to edit. Sector is a dropdown. Price/Qty have validation.",
                color="gray.400",
            ),
            toolbar("editable_grid"),
            AGGrid.create(
                column_defs=DemoState.editable_column_defs,
                row_data=DemoState.editable_data,
                grid_id="editable_grid",
                theme="ag-theme-balham-dark",
                height="400px",
                width="100%",
                on_cell_edit=DemoState.handle_cell_edit,
            ),
            notification_panel(),
            spacing="4",
            padding="4",
            width="100%",
        ),
        bg="gray.950",
        min_height="100vh",
    )


def grouped_page() -> rx.Component:
    """Grouped grid page - row grouping with aggregation."""
    return rx.box(
        nav_bar(),
        rx.vstack(
            rx.heading("Grouped Grid", size="5"),
            rx.text(
                "Data grouped by Sector. Price shows average, Qty shows sum.",
                color="gray.400",
            ),
            toolbar("grouped_grid"),
            AGGrid.create(
                column_defs=DemoState.grouped_column_defs,
                row_data=DemoState.grouped_data,
                grid_id="grouped_grid",
                theme="ag-theme-balham-dark",
                height="500px",
                width="100%",
            ),
            spacing="4",
            padding="4",
            width="100%",
        ),
        bg="gray.950",
        min_height="100vh",
    )


def streaming_page() -> rx.Component:
    """Streaming data page - mock real-time updates."""
    return rx.box(
        nav_bar(),
        rx.vstack(
            rx.heading("Streaming Data", size="5"),
            rx.text(
                "Simulates real-time price updates. Toggle auto-refresh or update manually.",
                color="gray.400",
            ),
            rx.hstack(
                rx.button(
                    rx.cond(DemoState.auto_refresh, "⏸ Stop", "▶ Start Auto"),
                    on_click=DemoState.toggle_auto_refresh,
                    color_scheme=rx.cond(DemoState.auto_refresh, "red", "green"),
                    variant="solid",
                ),
                rx.button(
                    "🔄 Manual Refresh",
                    on_click=DemoState.manual_refresh,
                    variant="outline",
                ),
                rx.button(
                    "↺ Reset",
                    on_click=DemoState.reset_streaming_data,
                    variant="outline",
                ),
                rx.spacer(),
                rx.badge(f"Updates: {DemoState.update_count}", color_scheme="blue"),
                spacing="2",
                padding="2",
            ),
            AGGrid.create(
                column_defs=DemoState.basic_column_defs,
                row_data=DemoState.streaming_data,
                grid_id="streaming_grid",
                theme="ag-theme-balham-dark",
                height="500px",
                width="100%",
            ),
            spacing="4",
            padding="4",
            width="100%",
        ),
        bg="gray.950",
        min_height="100vh",
    )


# =============================================================================
# APP SETUP
# =============================================================================

app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="blue",
    )
)

app.add_page(basic_page, route="/", title="Basic Grid")
app.add_page(editable_page, route="/editable", title="Editable Grid")
app.add_page(grouped_page, route="/grouped", title="Grouped Grid")
app.add_page(streaming_page, route="/streaming", title="Streaming Data")
