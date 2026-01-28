"""
18 - Performance Testing Page - 1000-row stress test.

Requirement 18: Performance Testing with Large Datasets
AG Grid Feature: Virtual scrolling + row virtualization
"""

import reflex as rx
import random

from reflex_ag_grid import ag_grid

from ..components import nav_bar


class PerfTestState(rx.State):
    """State for performance testing demo."""

    data: list[dict] = []
    row_count: int = 1000
    test_status: str = "Ready"
    last_render_time: str = "—"

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
        self.test_status = f"✅ Loaded {self.row_count} rows"

    def clear_data(self):
        """Clear the dataset."""
        self.data = []
        self.test_status = "Cleared"

    def set_row_count(self, value: str):
        """Set number of rows to generate."""
        try:
            self.row_count = int(value)
        except ValueError:
            pass


def perf_test_page() -> rx.Component:
    """Performance Testing demo page.

    Features:
    - Generate 100 to 10,000+ rows
    - Virtual scrolling (AG Grid Enterprise)
    - Row virtualization for smooth scrolling
    - Stress test for rendering performance
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("18 - Performance Testing", size="6"),
        rx.text("Large dataset stress test with 1000+ rows"),
        rx.callout(
            "AG Grid uses virtual scrolling to handle large datasets efficiently. "
            "Only visible rows are rendered. Try 1000, 5000, or 10000 rows!",
            icon="info",
        ),
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
            rx.badge(PerfTestState.test_status, color_scheme="blue"),
            spacing="3",
        ),
        rx.text(f"Current rows: {PerfTestState.data.length()}", size="2", color="gray"),
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
            height="55vh",
        ),
        rx.box(
            rx.heading("Virtual Scrolling Benefits:", size="4"),
            rx.unordered_list(
                rx.list_item("Only visible rows are rendered"),
                rx.list_item("Smooth scrolling for 10,000+ rows"),
                rx.list_item("Low memory footprint"),
                rx.list_item("Fast initial render"),
            ),
            padding="3",
            background="var(--gray-2)",
            border_radius="8px",
        ),
        padding="4",
        spacing="3",
    )
