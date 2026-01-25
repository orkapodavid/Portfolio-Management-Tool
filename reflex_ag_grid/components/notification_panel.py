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


def _get_grid_ref(grid_id: str) -> str:
    """Get the ref name for a grid ID."""
    # Reflex formats refs as 'ref_' + id
    return f"ref_{grid_id}"


def _jump_to_row_script(grid_id: str, row_id_expr: str, flash: bool = True) -> str:
    """
    Generate JS script to jump to a row and optionally flash it.

    Args:
        grid_id: The grid ID
        row_id_expr: The row ID expression (can be dynamic)
        flash: Whether to flash the row after scrolling
    """
    ref = _get_grid_ref(grid_id)
    script = f"""
    (() => {{
        const gridRef = refs['{ref}'];
        if (gridRef && gridRef.current && gridRef.current.api) {{
            const api = gridRef.current.api;
            const rowId = {row_id_expr};
            const node = api.getRowNode(rowId);
            if (node) {{
                api.ensureNodeVisible(node, 'middle');
                {"api.flashCells({rowNodes: [node]});" if flash else ""}
            }} else {{
                console.warn('Row not found:', rowId);
            }}
        }} else {{
            console.warn('Grid API not available for:', '{grid_id}');
        }}
    }})()
    """
    return script


def notification_panel(
    notifications: rx.Var[list[dict]],
    grid_id: str,
    on_clear: rx.EventHandler | None = None,
    title: str = "Notifications",
    width: str = "300px",
    empty_message: str = "No notifications",
    flash_on_jump: bool = True,
    route: str | None = None,
) -> rx.Component:
    """
    Reusable notification panel with jump-to-row functionality.

    Args:
        notifications: List of notification dicts with keys:
            - message (str): Notification text
            - row_id (str): Row ID to jump to when clicked
            - level (str): "info", "warning", "error", or "success"
            - route (optional str): Route to navigate to before jumping
        grid_id: ID of the AG Grid to jump to
        on_clear: Optional event handler for clear button
        title: Panel title (default: "Notifications")
        width: Panel width (default: "300px")
        empty_message: Message when no notifications
        flash_on_jump: Whether to flash the row after scrolling (default: True)
        route: Default route to navigate to (can be overridden per notification)

    Returns:
        rx.Component: The notification panel component
    """
    ref = _get_grid_ref(grid_id)

    def notification_item(n: rx.Var[dict]) -> rx.Component:
        """Single notification item with jump button."""
        # Build the jump script - row_id comes from the notification dict
        jump_script = f"""
        (() => {{
            const gridRef = refs['{ref}'];
            const rowId = {n}['row_id'];
            
            // First check if we need to navigate
            const notifRoute = {n}['route'];
            if (notifRoute && window.location.pathname !== notifRoute) {{
                // Navigate and then jump after a delay
                window.location.href = notifRoute;
                return;
            }}
            
            if (gridRef && gridRef.current && gridRef.current.api) {{
                const api = gridRef.current.api;
                const node = api.getRowNode(rowId);
                if (node) {{
                    api.ensureNodeVisible(node, 'middle');
                    {"api.flashCells({rowNodes: [node]});" if flash_on_jump else ""}
                }} else {{
                    console.warn('Row not found:', rowId);
                }}
            }} else {{
                console.warn('Grid API not available');
            }}
        }})()
        """

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
                rx.text(n["message"], size="2", flex="1"),
                rx.button(
                    "→",
                    size="1",
                    title="Jump to row",
                    on_click=rx.call_script(jump_script),
                ),
                spacing="2",
                width="100%",
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


def jump_to_row(grid_id: str, row_id: str, flash: bool = True) -> rx.event.EventSpec:
    """
    Create an event to jump to a specific row in a grid.

    Args:
        grid_id: The grid ID
        row_id: The row ID to jump to
        flash: Whether to flash the row (default: True)

    Returns:
        An rx.call_script event for scrolling to the row
    """
    return rx.call_script(_jump_to_row_script(grid_id, f"'{row_id}'", flash))
