"""
10 - WebSocket Page - Demonstrates real-time WebSocket updates.

Requirement 10: WebSocket publishing
AG Grid Feature: Reflex WebSocket state updates
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_basic_columns
from ..components import nav_bar, notification_panel


def websocket_page() -> rx.Component:
    """WebSocket demo page.

    Features:
    - Real-time price updates via WebSocket
    - Start/Stop streaming toggle
    - Cell flash on change
    - Notification panel for significant changes
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("10 - WebSocket", size="6"),
        rx.text("Requirement 10: WebSocket publishing"),
        rx.callout(
            "Click 'Start Streaming' to receive real-time updates. "
            "Cells will flash when values change.",
            icon="info",
        ),
        rx.hstack(
            rx.cond(
                DemoState.is_streaming,
                rx.button(
                    "⏹️ Stop Streaming",
                    color_scheme="red",
                    on_click=DemoState.toggle_streaming,
                ),
                rx.button(
                    "▶️ Start Streaming",
                    color_scheme="green",
                    on_click=DemoState.toggle_streaming,
                ),
            ),
            rx.button(
                "Manual Update",
                on_click=DemoState.simulate_price_update,
            ),
            rx.badge(
                rx.cond(DemoState.is_streaming, "LIVE", "STOPPED"),
                color_scheme=rx.cond(DemoState.is_streaming, "green", "gray"),
            ),
        ),
        rx.hstack(
            ag_grid(
                id="websocket_grid",
                row_data=DemoState.data,
                column_defs=get_basic_columns(),
                row_id_key="id",
                enable_cell_change_flash=True,
                theme="quartz",
                width="60vw",
                height="60vh",
                on_grid_ready=DemoState.execute_pending_highlight("websocket_grid"),
            ),
            notification_panel(),
            spacing="4",
        ),
        # Polling for streaming
        rx.cond(
            DemoState.is_streaming,
            rx.moment(interval=2000, on_change=DemoState.simulate_price_update),
            rx.fragment(),
        ),
        rx.text(
            "Uses Reflex WebSocket for real-time state sync.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
