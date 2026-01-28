"""
20 - Overlays Page - Demonstrates loading and no-rows overlays.

Requirement 20: Loading/No-Rows Overlays
AG Grid Feature: overlayLoadingTemplate + overlayNoRowsTemplate
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..columns import get_basic_columns
from ..components import nav_bar


class OverlayState(rx.State):
    """State for overlay demo."""

    data: list[dict] = []
    is_loading: bool = False

    async def load_data(self):
        """Simulate loading data with delay."""
        import asyncio

        self.is_loading = True
        self.data = []
        yield

        await asyncio.sleep(2)  # Simulate API delay

        self.data = [
            {
                "id": "1",
                "symbol": "AAPL",
                "company": "Apple Inc.",
                "sector": "Technology",
                "price": 175.5,
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
                "price": 378.9,
                "qty": 75,
                "change": 0.8,
            },
        ]
        self.is_loading = False

    def clear_data(self):
        """Clear data to show no-rows overlay."""
        self.data = []
        self.is_loading = False


def overlays_page() -> rx.Component:
    """Overlays demo page.

    Features:
    - Loading overlay during data fetch
    - No-rows overlay when data is empty
    - Custom overlay templates
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("20 - Overlays", size="6"),
        rx.text("Loading and No-Rows overlays"),
        rx.callout(
            "Click 'Load Data' to see the loading overlay, then 'Clear' to see the no-rows overlay. "
            "Overlays provide visual feedback during async operations.",
            icon="info",
        ),
        rx.hstack(
            rx.button(
                "📂 Load Data",
                on_click=OverlayState.load_data,
                color_scheme="green",
            ),
            rx.button(
                "🗑️ Clear",
                on_click=OverlayState.clear_data,
                color_scheme="gray",
            ),
            rx.cond(
                OverlayState.is_loading,
                rx.badge("Loading...", color_scheme="orange"),
                rx.cond(
                    OverlayState.data.length() > 0,
                    rx.badge(
                        f"{OverlayState.data.length()} rows", color_scheme="green"
                    ),
                    rx.badge("No data", color_scheme="gray"),
                ),
            ),
            spacing="3",
        ),
        ag_grid(
            id="overlays_grid",
            row_data=OverlayState.data,
            column_defs=get_basic_columns(),
            row_id_key="id",
            theme="quartz",
            width="90vw",
            height="50vh",
            loading=OverlayState.is_loading,
            overlay_loading_template="<span class='ag-overlay-loading-center'>Loading data...</span>",
            overlay_no_rows_template="<span style='padding: 20px;'>No rows to display. Click 'Load Data' to fetch records.</span>",
        ),
        rx.box(
            rx.heading("Overlay Configuration:", size="4"),
            rx.code_block(
                """ag_grid(
    loading=State.is_loading,  # Show loading overlay
    overlay_loading_template="<span>Loading...</span>",
    overlay_no_rows_template="<span>No data available</span>",
)""",
                language="python",
            ),
            padding="3",
            background="var(--gray-2)",
            border_radius="8px",
        ),
        padding="4",
        spacing="3",
    )
