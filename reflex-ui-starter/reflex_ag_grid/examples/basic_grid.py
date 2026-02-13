"""
Basic AG Grid Example

Demonstrates:
- Column definitions with various types
- Cell editing with validation
- Formatters and cell styling
- Event handling
- Notification system
"""

import reflex as rx
from reflex_ag_grid import AGGrid, AGGridStateMixin, ColumnDef, ColumnType


class ExampleState(rx.State, AGGridStateMixin):
    """Example state demonstrating AG Grid features."""

    # Sample data
    items: list[dict] = [
        {
            "id": "1",
            "symbol": "AAPL",
            "name": "Apple Inc.",
            "price": 178.50,
            "quantity": 100,
            "change": 2.35,
            "status": "Active",
        },
        {
            "id": "2",
            "symbol": "GOOGL",
            "name": "Alphabet Inc.",
            "price": 141.25,
            "quantity": 50,
            "change": -1.20,
            "status": "Active",
        },
        {
            "id": "3",
            "symbol": "MSFT",
            "name": "Microsoft Corp.",
            "price": 378.90,
            "quantity": 75,
            "change": 0.85,
            "status": "Pending",
        },
        {
            "id": "4",
            "symbol": "AMZN",
            "name": "Amazon.com Inc.",
            "price": 178.25,
            "quantity": 25,
            "change": -0.50,
            "status": "Active",
        },
        {
            "id": "5",
            "symbol": "TSLA",
            "name": "Tesla Inc.",
            "price": 248.50,
            "quantity": 30,
            "change": 5.75,
            "status": "Cancelled",
        },
    ]

    # Column definitions
    column_defs: list[dict] = [
        ColumnDef(
            field="id",
            header_name="ID",
            width=70,
            pinned="left",
        ).to_ag_grid_def(),
        ColumnDef(
            field="symbol",
            header_name="Symbol",
            width=100,
            cell_style={"fontWeight": "bold"},
        ).to_ag_grid_def(),
        ColumnDef(
            field="name",
            header_name="Company Name",
            min_width=180,
            flex=1,
            editable=True,
        ).to_ag_grid_def(),
        ColumnDef(
            field="price",
            header_name="Price",
            type=ColumnType.FLOAT,
            width=120,
            editable=True,
            formatter="currency",
            validation={"min": 0, "max": 10000},
        ).to_ag_grid_def(),
        ColumnDef(
            field="quantity",
            header_name="Qty",
            type=ColumnType.INTEGER,
            width=100,
            editable=True,
            formatter="number",
            validation={"min": 1, "max": 10000},
        ).to_ag_grid_def(),
        ColumnDef(
            field="change",
            header_name="Change %",
            type=ColumnType.FLOAT,
            width=120,
            formatter="percentage_value",
            cell_class_rules="traffic_light",
        ).to_ag_grid_def(),
        ColumnDef(
            field="status",
            header_name="Status",
            type=ColumnType.ENUM,
            width=120,
            editable=True,
            enum_values=["Active", "Pending", "Cancelled"],
            renderer="status_badge",
        ).to_ag_grid_def(),
    ]

    def handle_cell_edit(self, data: dict):
        """Handle cell edit events."""
        row_id = data.get("rowId", "")
        field = data.get("field", "")
        old_value = data.get("oldValue")
        new_value = data.get("newValue")

        # Update local state
        self.update_row_data("items", row_id, {field: new_value})

        # Add success notification
        self.add_notification(
            message=f"Updated {field}: {old_value} → {new_value}",
            row_id=row_id,
            notification_type="success",
        )

    def handle_row_double_click(self, data: dict):
        """Handle row double-click."""
        row_id = data.get("rowId", "")
        symbol = data.get("rowData", {}).get("symbol", "")

        self.add_notification(
            message=f"Double-clicked: {symbol}",
            row_id=row_id,
            notification_type="info",
        )

    def do_export_excel(self):
        """Export to Excel."""
        return self.export_to_excel(grid_id="example_grid")

    def do_export_csv(self):
        """Export to CSV."""
        return self.export_to_csv(grid_id="example_grid")

    def do_reset_columns(self):
        """Reset column state."""
        return self.reset_column_state(grid_id="example_grid")


def toolbar() -> rx.Component:
    """Toolbar with export buttons."""
    return rx.hstack(
        rx.button(
            rx.icon("file-spreadsheet", size=16),
            "Excel",
            on_click=ExampleState.do_export_excel,
            variant="outline",
        ),
        rx.button(
            rx.icon("file-text", size=16),
            "CSV",
            on_click=ExampleState.do_export_csv,
            variant="outline",
        ),
        rx.button(
            rx.icon("columns", size=16),
            "Reset Columns",
            on_click=ExampleState.do_reset_columns,
            variant="outline",
        ),
        spacing="2",
        padding="3",
    )


def example_grid() -> rx.Component:
    """The AG Grid component."""
    return AGGrid.create(
        column_defs=ExampleState.column_defs,
        row_data=ExampleState.items,
        grid_id="example_grid",
        theme="ag-theme-balham-dark",
        height="400px",
        width="100%",
        on_cell_edit=ExampleState.handle_cell_edit,
        on_row_double_click=ExampleState.handle_row_double_click,
        on_selection_change=ExampleState.handle_selection_change,
    )


def notification_list() -> rx.Component:
    """Display notifications."""
    return rx.cond(
        ExampleState.notifications.length() > 0,
        rx.vstack(
            rx.text("Notifications", font_weight="bold"),
            rx.foreach(
                ExampleState.notifications[:5],
                lambda n: rx.hstack(
                    rx.badge(
                        n["type"],
                        color_scheme=rx.cond(
                            n["type"] == "success",
                            "green",
                            rx.cond(n["type"] == "error", "red", "blue"),
                        ),
                    ),
                    rx.text(n["message"], font_size="sm"),
                    rx.spacer(),
                    rx.button(
                        rx.icon("x", size=12),
                        size="xs",
                        variant="ghost",
                        on_click=lambda: ExampleState.clear_notification(n["id"]),
                    ),
                    width="100%",
                    padding="2",
                    bg="gray.800",
                    border_radius="md",
                ),
            ),
            spacing="2",
            width="100%",
        ),
        rx.box(),
    )


def index() -> rx.Component:
    """Main page."""
    return rx.box(
        rx.vstack(
            rx.heading("AG Grid Example", size="lg"),
            toolbar(),
            example_grid(),
            notification_list(),
            spacing="4",
            width="100%",
        ),
        padding="20px",
        bg="gray.950",
        min_height="100vh",
    )


# App setup
app = rx.App(
    theme=rx.theme(
        appearance="dark",
        accent_color="blue",
    )
)
app.add_page(index)
