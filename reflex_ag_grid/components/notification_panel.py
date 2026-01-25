"""
Reusable Notification Panel Component

A notification panel that displays notifications with jump-to-row functionality.
Works with AG Grid to scroll to and flash specific rows when notifications are clicked.

Usage:
    from reflex_ag_grid.components.notification_panel import notification_panel

    def my_page():
        return rx.hstack(
            ag_grid(id="my_grid", ...),
            notification_panel(
                notifications=MyState.notifications,
                grid_id="my_grid",
                on_clear=MyState.clear_notifications,
            ),
        )
"""

import reflex as rx


def notification_panel(
    notifications: rx.Var[list[dict]],
    grid_id: str,
    on_clear: rx.EventHandler | None = None,
    title: str = "Notifications",
    width: str = "300px",
    empty_message: str = "No notifications",
) -> rx.Component:
    """
    Reusable notification panel with jump-to-row functionality.

    Args:
        notifications: List of notification dicts with keys:
            - message (str): Notification text
            - row_id (str): Row ID to jump to when clicked
            - level (str): "info", "warning", "error", or "success"
        grid_id: ID of the AG Grid to jump to
        on_clear: Optional event handler for clear button
        title: Panel title (default: "Notifications")
        width: Panel width (default: "300px")
        empty_message: Message when no notifications (default: "No notifications")

    Returns:
        rx.Component: The notification panel component
    """

    def notification_item(n: rx.Var[dict]) -> rx.Component:
        """Single notification item with jump button."""
        return rx.card(
            rx.hstack(
                rx.badge(
                    n["level"],
                    color_scheme=rx.match(
                        n["level"],
                        ("warning", "orange"),
                        ("success", "green"),
                        ("error", "red"),
                        "blue",  # default for "info"
                    ),
                ),
                rx.text(n["message"], size="2"),
                rx.button(
                    "→",
                    size="1",
                    title="Jump to row",
                    on_click=rx.call_script(
                        f"(() => {{"
                        f"  const grid = document.querySelector('#{grid_id}');"
                        f"  if (grid && grid.__agGridApi) {{"
                        f"    const api = grid.__agGridApi;"
                        f"    const node = api.getRowNode('{n['row_id']}');"
                        f"    if (node) {{"
                        f"      api.ensureNodeVisible(node, 'middle');"
                        f"      api.flashCells({{rowNodes: [node]}});"
                        f"    }}"
                        f"  }}"
                        f"}})()"
                    ),
                ),
                spacing="2",
            ),
            size="1",
        )

    header = rx.hstack(
        rx.heading(title, size="4"),
        rx.cond(
            on_clear is not None,
            rx.button("Clear", size="1", on_click=on_clear),
            rx.fragment(),
        ),
        justify="between",
        width="100%",
    )

    content = rx.cond(
        notifications.length() > 0,
        rx.vstack(
            rx.foreach(notifications, notification_item),
            spacing="1",
            width="100%",
        ),
        rx.text(empty_message, color="gray", size="2"),
    )

    return rx.vstack(
        header,
        content,
        width=width,
        padding="2",
        border="1px solid var(--gray-5)",
        border_radius="8px",
    )


# Type alias for notification dict structure
class NotificationDict:
    """
    Expected notification dictionary structure.

    Attributes:
        message (str): The notification message text
        row_id (str): ID of the row to jump to
        level (str): One of "info", "warning", "error", "success"
    """

    message: str
    row_id: str
    level: str
