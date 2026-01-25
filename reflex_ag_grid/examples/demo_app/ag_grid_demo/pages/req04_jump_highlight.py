"""
04 - Jump & Highlight Page - Demonstrates notification jump and highlight.

Requirement 4: Notification jump & highlight
AG Grid Feature: ensureNodeVisible() + flashCells()
"""

import reflex as rx

from ..state import DemoState
from ..components import nav_bar


def jump_highlight_page() -> rx.Component:
    """Jump & Highlight demo page.

    Features:
    - Click button to navigate and highlight row
    - Row scrolls into view
    - Row flashes to draw attention
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("04 - Jump & Highlight", size="6"),
        rx.text("Requirement 4: Notification jump & highlight"),
        rx.callout(
            "Click a button below to navigate to the Streaming page "
            "and automatically scroll to and highlight a specific row.",
            icon="info",
        ),
        rx.vstack(
            rx.heading("Jump to Row in Streaming Page", size="4"),
            rx.hstack(
                rx.button(
                    "Jump to AAPL",
                    on_click=DemoState.navigate_and_highlight(
                        "/10-websocket", "websocket_grid", "0"
                    ),
                    color_scheme="blue",
                ),
                rx.button(
                    "Jump to GOOGL",
                    on_click=DemoState.navigate_and_highlight(
                        "/10-websocket", "websocket_grid", "1"
                    ),
                    color_scheme="green",
                ),
                rx.button(
                    "Jump to MSFT",
                    on_click=DemoState.navigate_and_highlight(
                        "/10-websocket", "websocket_grid", "2"
                    ),
                    color_scheme="purple",
                ),
                rx.button(
                    "Jump to XOM",
                    on_click=DemoState.navigate_and_highlight(
                        "/10-websocket", "websocket_grid", "7"
                    ),
                    color_scheme="orange",
                ),
            ),
            padding="4",
            background="var(--gray-2)",
            border_radius="8px",
        ),
        rx.text(
            "Uses ensureNodeVisible() to scroll and flashCells() to highlight.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
