"""
Notification Panel Component - Shows notifications with jump-to-row.

Implements Req 4 (jump & highlight) and Req 6 (notification publisher).
"""

import reflex as rx

from ..state import DemoState


def notification_panel() -> rx.Component:
    """Notification panel with jump-to-row functionality.

    Features:
    - Shows last 5 notifications
    - Color-coded by level (info, warning, success, error)
    - Jump button to scroll and flash the related row
    - Clear button to dismiss all notifications
    """

    def notification_item(n: rx.Var[dict]) -> rx.Component:
        """Single notification with jump button."""
        return rx.card(
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
                rx.text(n["message"], size="2", flex="1"),
                rx.button(
                    "→",
                    size="1",
                    on_click=DemoState.jump_to_row(n["row_id"]),
                ),
            ),
            size="1",
        )

    return rx.vstack(
        rx.hstack(
            rx.heading("Notifications", size="4"),
            rx.button("Clear", size="1", on_click=DemoState.clear_notifications),
        ),
        rx.cond(
            DemoState.notifications.length() > 0,
            rx.vstack(
                rx.foreach(DemoState.notifications, notification_item),
                spacing="1",
            ),
            rx.text("No notifications", color="gray", size="2"),
        ),
        width="300px",
        padding="2",
        border="1px solid var(--gray-5)",
        border_radius="8px",
    )
