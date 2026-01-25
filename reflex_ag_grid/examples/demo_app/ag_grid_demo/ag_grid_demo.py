"""
AG Grid Demo App - Multi-page demo showcasing all AG Grid features.

Demonstrates all 15 requirements from the AG Grid Traceability Matrix.
"""

import random

import reflex as rx

from reflex_ag_grid import ag_grid


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
        "active": True,
    },
    {
        "id": "2",
        "symbol": "GOOGL",
        "company": "Alphabet Inc.",
        "sector": "Technology",
        "price": 140.25,
        "qty": 50,
        "change": -1.2,
        "active": True,
    },
    {
        "id": "3",
        "symbol": "MSFT",
        "company": "Microsoft Corp.",
        "sector": "Technology",
        "price": 378.90,
        "qty": 75,
        "change": 0.8,
        "active": True,
    },
    {
        "id": "4",
        "symbol": "JPM",
        "company": "JPMorgan Chase",
        "sector": "Finance",
        "price": 195.00,
        "qty": 200,
        "change": 1.5,
        "active": False,
    },
    {
        "id": "5",
        "symbol": "GS",
        "company": "Goldman Sachs",
        "sector": "Finance",
        "price": 385.75,
        "qty": 30,
        "change": -0.5,
        "active": True,
    },
    {
        "id": "6",
        "symbol": "JNJ",
        "company": "Johnson & Johnson",
        "sector": "Healthcare",
        "price": 155.30,
        "qty": 120,
        "change": 0.3,
        "active": True,
    },
    {
        "id": "7",
        "symbol": "PFE",
        "company": "Pfizer Inc.",
        "sector": "Healthcare",
        "price": 28.50,
        "qty": 500,
        "change": -2.1,
        "active": False,
    },
    {
        "id": "8",
        "symbol": "XOM",
        "company": "Exxon Mobil",
        "sector": "Energy",
        "price": 105.20,
        "qty": 150,
        "change": 3.2,
        "active": True,
    },
]

SECTORS = ["Technology", "Finance", "Healthcare", "Energy"]


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def get_basic_columns():
    """Basic column definitions."""
    return [
        ag_grid.column_def(
            field="symbol",
            header_name="Symbol",
            sortable=True,
            filter="agTextColumnFilter",
        ),
        ag_grid.column_def(field="company", header_name="Company", flex=1),
        ag_grid.column_def(
            field="sector", header_name="Sector", filter="agSetColumnFilter"
        ),
        ag_grid.column_def(
            field="price",
            header_name="Price",
            sortable=True,
            filter="agNumberColumnFilter",
        ),
        ag_grid.column_def(field="qty", header_name="Quantity", sortable=True),
        ag_grid.column_def(field="change", header_name="Change %", sortable=True),
    ]


def get_editable_columns():
    """Columns with different cell editors (Req 11)."""
    return [
        ag_grid.column_def(field="symbol", header_name="Symbol", editable=False),
        ag_grid.column_def(field="company", header_name="Company", editable=True),
        ag_grid.column_def(
            field="sector",
            header_name="Sector",
            editable=True,
            cell_editor="agSelectCellEditor",
            cell_editor_params={"values": SECTORS},
        ),
        ag_grid.column_def(
            field="price",
            header_name="Price",
            editable=True,
            cell_editor="agNumberCellEditor",
        ),
        ag_grid.column_def(field="qty", header_name="Quantity", editable=True),
        ag_grid.column_def(
            field="active",
            header_name="Active",
            editable=True,
            cell_editor="agCheckboxCellEditor",
            cell_renderer="agCheckboxCellRenderer",
        ),
    ]


def get_grouped_columns():
    """Columns with grouping support (Req 5)."""
    return [
        ag_grid.column_def(
            field="sector", header_name="Sector", row_group=True, hide=True
        ),
        ag_grid.column_def(field="symbol", header_name="Symbol", sortable=True),
        ag_grid.column_def(field="company", header_name="Company", flex=1),
        ag_grid.column_def(field="price", header_name="Price", agg_func="avg"),
        ag_grid.column_def(field="qty", header_name="Quantity", agg_func="sum"),
        ag_grid.column_def(field="change", header_name="Change %", agg_func="avg"),
    ]


# =============================================================================
# STATE
# =============================================================================


class DemoState(rx.State):
    """Demo application state."""

    data: list[dict] = SAMPLE_DATA
    selected_rows: list[dict] = []
    last_event: str = "None"
    notifications: list[dict] = []
    is_streaming: bool = False
    pause_on_edit: bool = False
    is_editing: bool = False
    search_text: str = ""

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
        """Handle cell value changes (Req 7 - validation feedback)."""
        # Simple validation example
        if field == "price":
            try:
                val = float(new_value)
                if val < 0:
                    self.last_event = f"❌ Validation error: Price cannot be negative"
                    return
            except ValueError:
                self.last_event = f"❌ Validation error: Invalid price value"
                return

        self.last_event = f"✅ Cell edit: row {row_index}, {field} = {new_value}"
        # Update data
        if 0 <= row_index < len(self.data):
            self.data[row_index][field] = new_value

    def on_editing_started(self, row_index: int, field: str):
        """Track when editing starts (Req 12) - automatically pauses updates."""
        self.is_editing = True
        self.pause_on_edit = True  # Auto-pause when editing starts
        self.last_event = f"✏️ Editing row {row_index}, field: {field}"

    def on_editing_stopped(self, row_index: int, field: str):
        """Track when editing stops - resumes updates."""
        self.is_editing = False
        self.pause_on_edit = False  # Auto-resume when editing stops
        self.last_event = f"✅ Finished editing row {row_index}"

    def add_notification(self, message: str, row_id: str, level: str = "info"):
        """Add a notification (Req 6)."""
        self.notifications = [
            {
                "id": len(self.notifications),
                "message": message,
                "row_id": row_id,
                "level": level,
            }
        ] + self.notifications[:4]  # Keep last 5

    def simulate_price_update(self):
        """Simulate streaming price update (Req 10, 14)."""
        if self.pause_on_edit and self.is_editing:
            return  # Skip update while editing (Req 12)

        # Random price change
        idx = random.randint(0, len(self.data) - 1)
        old_price = self.data[idx]["price"]
        change = random.uniform(-5, 5)
        new_price = round(old_price + change, 2)

        self.data[idx]["price"] = new_price
        self.data[idx]["change"] = round(change, 2)

        # Generate notification for significant changes
        if abs(change) > 3:
            level = "warning" if change < 0 else "success"
            self.add_notification(
                f"{self.data[idx]['symbol']}: ${old_price:.2f} → ${new_price:.2f}",
                self.data[idx]["id"],
                level,
            )

    def toggle_streaming(self):
        """Toggle streaming updates."""
        self.is_streaming = not self.is_streaming

    def toggle_pause_on_edit(self):
        """Toggle pause on edit mode."""
        self.pause_on_edit = not self.pause_on_edit

    def clear_notifications(self):
        """Clear all notifications."""
        self.notifications = []


# =============================================================================
# UI COMPONENTS
# =============================================================================


def nav_bar() -> rx.Component:
    """Navigation bar for demo pages."""
    return rx.hstack(
        rx.link("Basic", href="/"),
        rx.link("Editable", href="/editable"),
        rx.link("Grouped", href="/grouped"),
        rx.link("Streaming", href="/streaming"),
        rx.link("Range Select", href="/range"),
        rx.link("Column State", href="/column-state"),
        rx.link("Search", href="/search"),
        spacing="4",
        padding="3",
        background="var(--gray-2)",
        width="100%",
    )


def status_badge() -> rx.Component:
    """Status badge showing last event."""
    return rx.badge(DemoState.last_event, color_scheme="blue")


def notification_panel() -> rx.Component:
    """Notification panel with jump-to-row (Req 4, 6)."""
    return rx.vstack(
        rx.hstack(
            rx.heading("Notifications", size="4"),
            rx.button("Clear", size="1", on_click=DemoState.clear_notifications),
        ),
        rx.cond(
            DemoState.notifications.length() > 0,
            rx.vstack(
                rx.foreach(
                    DemoState.notifications,
                    lambda n: rx.card(
                        rx.hstack(
                            rx.badge(
                                n["level"],
                                color_scheme=rx.match(
                                    n["level"],
                                    ("warning", "orange"),
                                    ("success", "green"),
                                    ("error", "red"),
                                    "blue",
                                ),
                            ),
                            rx.text(n["message"], size="2"),
                            rx.button(
                                "→",
                                size="1",
                                on_click=rx.call_script(
                                    f"window.gridApi?.ensureNodeVisible(window.gridApi.getRowNode('{n['row_id']}'), 'middle'); "
                                    f"window.gridApi?.flashCells({{rowNodes: [window.gridApi.getRowNode('{n['row_id']}')]}})"
                                ),
                            ),
                        ),
                        size="1",
                    ),
                ),
                spacing="1",
            ),
            rx.text("No notifications", color="gray", size="2"),
        ),
        width="300px",
        padding="2",
        border="1px solid var(--gray-5)",
        border_radius="8px",
    )


# =============================================================================
# PAGES
# =============================================================================


def index() -> rx.Component:
    """Basic Grid page - Req 1 (context menu), Req 8 (copy), Req 9 (export)."""
    return rx.vstack(
        nav_bar(),
        rx.heading("Basic Grid", size="6"),
        rx.text("Features: Context menu (right-click), Copy, Export"),
        status_badge(),
        ag_grid(
            id="basic_grid",
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            row_selection="multiple",
            on_selection_changed=DemoState.on_selection_change,
            on_cell_clicked=DemoState.on_cell_click,
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        rx.hstack(
            rx.button(
                "Export Excel",
                on_click=rx.call_script("window.gridApi?.exportDataAsExcel()"),
            ),
            rx.button(
                "Export CSV",
                on_click=rx.call_script("window.gridApi?.exportDataAsCsv()"),
            ),
        ),
        padding="4",
        spacing="3",
    )


def editable_page() -> rx.Component:
    """Editable Grid page - Req 7 (validation), Req 11 (cell editors), Req 12 (pause on edit)."""
    return rx.vstack(
        nav_bar(),
        rx.heading("Editable Grid", size="6"),
        rx.text("Features: Different cell editors, Validation, Pause on edit"),
        rx.hstack(
            status_badge(),
            rx.cond(
                DemoState.is_editing,
                rx.badge("✏️ Editing", color_scheme="orange"),
                rx.badge("Ready", color_scheme="green"),
            ),
            rx.switch(
                checked=DemoState.pause_on_edit,
                on_change=DemoState.toggle_pause_on_edit,
            ),
            rx.text("Pause updates while editing"),
        ),
        ag_grid(
            id="editable_grid",
            row_data=DemoState.data,
            column_defs=get_editable_columns(),
            on_cell_value_changed=DemoState.on_cell_edit,
            on_cell_editing_started=DemoState.on_editing_started,
            on_cell_editing_stopped=DemoState.on_editing_stopped,
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        padding="4",
        spacing="3",
    )


def grouped_page() -> rx.Component:
    """Grouped Grid page - Req 5 (grouping & summary)."""
    return rx.vstack(
        nav_bar(),
        rx.heading("Grouped Grid", size="6"),
        rx.text("Features: Row grouping by sector, Aggregation (sum, avg)"),
        status_badge(),
        ag_grid(
            id="grouped_grid",
            row_data=DemoState.data,
            column_defs=get_grouped_columns(),
            group_default_expanded=-1,
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        padding="4",
        spacing="3",
    )


def streaming_page() -> rx.Component:
    """Streaming Data page - Req 3 (flash), Req 10 (WebSocket), Req 13 (Transaction), Req 14 (timing)."""
    return rx.vstack(
        nav_bar(),
        rx.heading("Streaming Data", size="6"),
        rx.text("Features: Cell flash on change, Real-time updates, Transaction API"),
        rx.hstack(
            rx.cond(
                DemoState.is_streaming,
                rx.button(
                    "Stop Streaming",
                    color_scheme="red",
                    on_click=DemoState.toggle_streaming,
                ),
                rx.button(
                    "Start Streaming",
                    color_scheme="green",
                    on_click=DemoState.toggle_streaming,
                ),
            ),
            rx.button("Manual Update", on_click=DemoState.simulate_price_update),
        ),
        rx.hstack(
            ag_grid(
                id="streaming_grid",
                row_data=DemoState.data,
                column_defs=get_basic_columns(),
                row_id_key="id",  # Critical for cell flash to work
                enable_cell_change_flash=True,
                theme="quartz",
                width="65vw",
                height="60vh",
            ),
            notification_panel(),
        ),
        # Polling for streaming (simple approach)
        rx.cond(
            DemoState.is_streaming,
            rx.moment(interval=2000, on_change=DemoState.simulate_price_update),
            rx.fragment(),
        ),
        padding="4",
        spacing="3",
    )


def range_page() -> rx.Component:
    """Range Selection page - Req 2 (bulk range selection)."""
    return rx.vstack(
        nav_bar(),
        rx.heading("Range Selection", size="6"),
        rx.text("Features: Multi-cell selection (Shift+click), Bulk updates"),
        status_badge(),
        ag_grid(
            id="range_grid",
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            enable_range_selection=True,
            row_selection="multiple",
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        rx.text("Hold Shift and drag to select a range of cells", color="gray"),
        padding="4",
        spacing="3",
    )


def column_state_page() -> rx.Component:
    """Column State page - Req 15 (save table format).

    Uses localStorage to persist column state across page refreshes.
    """
    grid_id = "column_state_grid"

    # JavaScript to find AG Grid API via React fiber tree
    # Uses a self-executing function pattern to safely access the Grid API
    get_api_js = """(function() {
        const wrapper = document.querySelector('.ag-root-wrapper');
        if (!wrapper) { alert('Grid not found'); return null; }
        const key = Object.keys(wrapper).find(k => k.startsWith('__reactFiber'));
        if (!key) { alert('React fiber not found'); return null; }
        let fiber = wrapper[key];
        while (fiber) {
            if (fiber.stateNode && fiber.stateNode.api) return fiber.stateNode.api;
            fiber = fiber.return;
        }
        alert('Grid API not found. Please wait and try again.');
        return null;
    })()"""

    return rx.vstack(
        nav_bar(),
        rx.heading("Column State Persistence", size="6"),
        rx.text("Features: Save/restore column widths, order, visibility"),
        rx.hstack(
            rx.button(
                "Save Column State",
                on_click=rx.call_script(
                    f"const api = {get_api_js}; "
                    "if (api) { "
                    "  const state = api.getColumnState(); "
                    "  localStorage.setItem('agGridColumnState', JSON.stringify(state)); "
                    "  alert('Column state saved! (' + state.length + ' columns)'); "
                    "}"
                ),
            ),
            rx.button(
                "Restore Column State",
                on_click=rx.call_script(
                    f"const api = {get_api_js}; "
                    "const state = localStorage.getItem('agGridColumnState'); "
                    "if (api && state) { "
                    "  api.applyColumnState({state: JSON.parse(state), applyOrder: true}); "
                    "  alert('Column state restored!'); "
                    "} else if (!state) { "
                    "  alert('No saved state found. Save first.'); "
                    "}"
                ),
            ),
            rx.button(
                "Reset Columns",
                on_click=rx.call_script(
                    f"const api = {get_api_js}; "
                    "if (api) { api.resetColumnState(); alert('Columns reset to default!'); }"
                ),
            ),
        ),
        ag_grid(
            id=grid_id,
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        rx.text(
            "Resize or reorder columns, then save. Refresh page and restore.",
            color="gray",
        ),
        padding="4",
        spacing="3",
    )


def search_page() -> rx.Component:
    """Search/Quick Filter page - Req 1.12 (global search)."""
    return rx.vstack(
        nav_bar(),
        rx.heading("Global Search / Quick Filter", size="6"),
        rx.text("Features: Filter all columns with a single text input"),
        rx.hstack(
            rx.input(
                placeholder="🔍 Search all columns...",
                value=DemoState.search_text,
                on_change=DemoState.set_search_text,
                width="400px",
            ),
            rx.button("Clear", on_click=DemoState.set_search_text(""), size="2"),
            rx.text("Filtering by: ", color="gray"),
            rx.cond(
                DemoState.search_text != "",
                rx.badge(DemoState.search_text, color_scheme="blue"),
                rx.text("(none)", color="gray"),
            ),
            spacing="3",
        ),
        ag_grid(
            id="search_grid",
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            quick_filter_text=DemoState.search_text,
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        rx.text(
            "Type to filter across Symbol, Company, Sector, Price, Quantity, and Change columns.",
            color="gray",
        ),
        padding="4",
        spacing="3",
    )


# =============================================================================
# APP
# =============================================================================

app = rx.App()
app.add_page(index, route="/", title="Basic Grid")
app.add_page(editable_page, route="/editable", title="Editable Grid")
app.add_page(grouped_page, route="/grouped", title="Grouped Grid")
app.add_page(streaming_page, route="/streaming", title="Streaming Data")
app.add_page(range_page, route="/range", title="Range Selection")
app.add_page(column_state_page, route="/column-state", title="Column State")
app.add_page(search_page, route="/search", title="Global Search")
