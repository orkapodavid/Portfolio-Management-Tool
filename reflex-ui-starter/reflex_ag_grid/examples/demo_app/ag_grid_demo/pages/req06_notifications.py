"""
06 - Notifications Page - Demonstrates notification publisher.

Requirement 6: Notification publisher
AG Grid Feature: Reflex State-based notifications
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_basic_columns
from ..components import nav_bar, notification_panel


def notifications_page() -> rx.Component:
    """Notifications demo page.

    Features:
    - Notification panel showing recent events
    - Color-coded by level (info, warning, success, error)
    - Click notification to jump to related row
    - Clear all notifications button
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("06 - Notifications", size="6"),
        rx.text("Requirement 6: Notification publisher"),
        rx.callout(
            "Click 'Generate Notification' to add a notification. "
            "Then click the arrow button to jump to that row.",
            icon="info",
        ),
        rx.hstack(
            rx.button(
                "Generate Notification",
                on_click=DemoState.simulate_price_update,
                color_scheme="blue",
            ),
            rx.button(
                "Clear All",
                on_click=DemoState.clear_notifications,
                color_scheme="gray",
            ),
        ),
        rx.hstack(
            ag_grid(
                id="notifications_grid",
                row_data=DemoState.data,
                column_defs=get_basic_columns(),
                row_id_key="id",
                enable_cell_change_flash=True,
                theme="quartz",
                width="60vw",
                height="60vh",
            ),
            notification_panel(),
            spacing="4",
        ),
        rx.text(
            "Notifications are managed via Reflex State. "
            "Each notification links to a specific row.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
