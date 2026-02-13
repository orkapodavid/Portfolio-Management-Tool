"""
18 - Performance Testing Page - 1000-row stress test with continuous CRUD.

Requirement 18: Performance Testing with Large Datasets
AG Grid Feature: Virtual scrolling + row virtualization + continuous updates
"""

import reflex as rx
import random

from reflex_ag_grid import ag_grid

from ..components import nav_bar


class PerfTestState(rx.State):
    """State for performance testing demo with continuous CRUD."""

    data: list[dict] = []
    row_count: int = 1000
    test_status: str = "Ready"
    is_running: bool = False

    # Statistics
    update_count: int = 0
    rows_added: int = 0
    rows_deleted: int = 0
    cells_updated: int = 0
    next_id: int = 0

    def generate_data(self):
        """Generate large dataset for performance testing."""
        self.test_status = f"Generating {self.row_count} rows..."

        symbols = [
            "AAPL",
            "GOOGL",
            "MSFT",
            "AMZN",
            "META",
            "TSLA",
            "NVDA",
            "JPM",
            "GS",
            "V",
        ]
        sectors = ["Technology", "Finance", "Healthcare", "Energy", "Consumer"]

        self.data = [
            {
                "id": f"row_{i}",
                "index": i + 1,
                "symbol": random.choice(symbols),
                "sector": random.choice(sectors),
                "price": round(random.uniform(50, 500), 2),
                "qty": random.randint(10, 1000),
                "change": round(random.uniform(-10, 10), 2),
                "volume": random.randint(100000, 10000000),
            }
            for i in range(self.row_count)
        ]
        self.next_id = self.row_count
        self.test_status = f"✅ Loaded {self.row_count} rows"
        self._reset_stats()

    def _reset_stats(self):
        """Reset statistics counters."""
        self.update_count = 0
        self.rows_added = 0
        self.rows_deleted = 0
        self.cells_updated = 0

    def clear_data(self):
        """Clear the dataset."""
        self.data = []
        self.test_status = "Cleared"
        self.is_running = False
        self._reset_stats()

    def set_row_count(self, value: str):
        """Set number of rows to generate."""
        try:
            self.row_count = int(value)
        except ValueError:
            pass

    def start_updates(self):
        """Start continuous CRUD updates."""
        if not self.data:
            self.test_status = "⚠️ Generate data first!"
            return
        self.is_running = True
        self.test_status = "🔄 Running CRUD updates..."

    def stop_updates(self):
        """Stop continuous CRUD updates."""
        self.is_running = False
        self.test_status = f"⏹️ Stopped after {self.update_count} cycles"

    def do_crud_tick(self):
        """Single tick of CRUD operations - called by rx.interval."""
        if not self.is_running or len(self.data) < 10:
            return

        symbols = ["AAPL", "GOOGL", "MSFT", "AMZN", "META", "TSLA", "NVDA"]
        sectors = ["Technology", "Finance", "Healthcare", "Energy", "Consumer"]

        # UPDATE: Randomly update 10-50 cells
        num_updates = random.randint(10, 50)
        for _ in range(min(num_updates, len(self.data))):
            idx = random.randint(0, len(self.data) - 1)
            self.data[idx]["price"] = round(random.uniform(50, 500), 2)
            self.data[idx]["change"] = round(random.uniform(-10, 10), 2)
        self.cells_updated += num_updates

        # CREATE: Randomly add 1-3 rows (10% chance)
        if random.random() < 0.1:
            for _ in range(random.randint(1, 3)):
                self.next_id += 1
                new_row = {
                    "id": f"row_{self.next_id}",
                    "index": self.next_id + 1,
                    "symbol": random.choice(symbols),
                    "sector": random.choice(sectors),
                    "price": round(random.uniform(50, 500), 2),
                    "qty": random.randint(10, 1000),
                    "change": round(random.uniform(-10, 10), 2),
                    "volume": random.randint(100000, 10000000),
                }
                self.data = self.data + [new_row]
                self.rows_added += 1

        # DELETE: Randomly delete 1-2 rows (5% chance)
        if random.random() < 0.05 and len(self.data) > 100:
            for _ in range(random.randint(1, 2)):
                idx = random.randint(0, len(self.data) - 1)
                self.data = self.data[:idx] + self.data[idx + 1 :]
                self.rows_deleted += 1

        self.update_count += 1


def perf_test_page() -> rx.Component:
    """Performance Testing demo page with continuous CRUD.

    Features:
    - Generate 100 to 10,000+ rows
    - Virtual scrolling (AG Grid Enterprise)
    - Continuous random CRUD operations
    - Live statistics dashboard
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("18 - Performance Testing", size="6"),
        rx.text("Large dataset stress test with continuous CRUD operations"),
        rx.callout(
            "AG Grid uses virtual scrolling to handle large datasets. "
            "Use 'Start CRUD' to continuously add/update/delete random rows!",
            icon="info",
        ),
        # Row generation controls
        rx.hstack(
            rx.text("Rows:", weight="bold"),
            rx.select(
                ["100", "500", "1000", "5000", "10000"],
                value=PerfTestState.row_count.to_string(),
                on_change=PerfTestState.set_row_count,
            ),
            rx.button(
                "⚡ Generate Data",
                on_click=PerfTestState.generate_data,
                color_scheme="green",
            ),
            rx.button(
                "🗑️ Clear",
                on_click=PerfTestState.clear_data,
                color_scheme="gray",
            ),
            spacing="3",
        ),
        # CRUD controls
        rx.hstack(
            rx.button(
                rx.cond(PerfTestState.is_running, "⏹️ Stop CRUD", "▶️ Start CRUD"),
                on_click=rx.cond(
                    PerfTestState.is_running,
                    PerfTestState.stop_updates,
                    PerfTestState.start_updates,
                ),
                color_scheme=rx.cond(PerfTestState.is_running, "red", "blue"),
            ),
            rx.badge(PerfTestState.test_status, color_scheme="purple"),
            spacing="3",
        ),
        # Statistics
        rx.hstack(
            rx.text(f"Rows: {PerfTestState.data.length()}", size="2"),
            rx.badge(f"Cycles: {PerfTestState.update_count}", color_scheme="gray"),
            rx.badge(f"➕ Added: {PerfTestState.rows_added}", color_scheme="green"),
            rx.badge(f"🗑️ Deleted: {PerfTestState.rows_deleted}", color_scheme="red"),
            rx.badge(f"✏️ Updated: {PerfTestState.cells_updated}", color_scheme="blue"),
            spacing="2",
        ),
        # Interval for CRUD updates (200ms = 5 updates/second)
        rx.cond(
            PerfTestState.is_running,
            rx.moment(interval=200, on_change=PerfTestState.do_crud_tick),
            rx.fragment(),
        ),
        ag_grid(
            id="perf_test_grid",
            row_data=PerfTestState.data,
            column_defs=[
                {"field": "index", "headerName": "#", "width": 70},
                {"field": "symbol", "headerName": "Symbol", "width": 100},
                {"field": "sector", "headerName": "Sector", "width": 120},
                {"field": "price", "headerName": "Price", "width": 100},
                {"field": "qty", "headerName": "Quantity", "width": 100},
                {"field": "change", "headerName": "Change", "width": 100},
                {"field": "volume", "headerName": "Volume", "width": 120},
            ],
            row_id_key="id",
            enable_cell_change_flash=True,
            theme="quartz",
            width="90vw",
            height="50vh",
        ),
        rx.box(
            rx.heading("Continuous CRUD Features:", size="4"),
            rx.unordered_list(
                rx.list_item("UPDATE: 10-50 random cells per tick"),
                rx.list_item("CREATE: 1-3 new rows (10% chance)"),
                rx.list_item("DELETE: 1-2 rows removed (5% chance)"),
                rx.list_item("Cell flashing shows all changes"),
            ),
            padding="3",
            background="var(--gray-2)",
            border_radius="8px",
        ),
        padding="4",
        spacing="3",
    )
