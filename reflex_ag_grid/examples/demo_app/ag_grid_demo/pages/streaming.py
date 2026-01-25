"""
Streaming Data Page - Demonstrates real-time updates and cell flashing.

Requirements:
- Req 3: Blinking cell changes
- Req 10: WebSocket publishing
- Req 13: Cell-by-cell update (Transaction API)
- Req 14: Update timing
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_basic_columns
from ..components import nav_bar, notification_panel


def streaming_page() -> rx.Component:
    """Streaming Data page with real-time updates.

    Features:
    - Cell flash on value change
    - Start/Stop streaming toggle
    - Manual update trigger
    - Notification panel with jump-to-row
    """
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
                on_grid_ready=DemoState.execute_pending_highlight("streaming_grid"),
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
