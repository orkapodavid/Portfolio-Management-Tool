"""
Jump Demo Page - Demonstrates cross-page navigation with row highlighting.

Requirements:
- Req 4: Notification jump & highlight
"""

import reflex as rx

from ..state import DemoState
from ..components import nav_bar


def jump_demo_page() -> rx.Component:
    """Cross-page navigation demo.

    Features:
    - Navigate to different page and highlight row
    - Uses pending_highlight state
    - Row flashes on arrival
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("Cross-Page Jump Demo", size="6"),
        rx.text("Click a button to navigate to a page and highlight a specific row."),
        rx.vstack(
            rx.heading("Jump to Streaming Page", size="4"),
            rx.hstack(
                rx.button(
                    "Jump to AAPL",
                    on_click=DemoState.navigate_and_highlight(
                        "/streaming", "streaming_grid", "0"
                    ),
                ),
                rx.button(
                    "Jump to GOOGL",
                    on_click=DemoState.navigate_and_highlight(
                        "/streaming", "streaming_grid", "1"
                    ),
                ),
                rx.button(
                    "Jump to MSFT",
                    on_click=DemoState.navigate_and_highlight(
                        "/streaming", "streaming_grid", "2"
                    ),
                ),
                rx.button(
                    "Jump to XOM",
                    on_click=DemoState.navigate_and_highlight(
                        "/streaming", "streaming_grid", "7"
                    ),
                ),
            ),
            padding="4",
            background="var(--gray-2)",
            border_radius="8px",
        ),
        rx.callout(
            "Click any button above. You will be redirected to the Streaming page "
            "and the selected row will flash automatically.",
            icon="info",
        ),
        padding="4",
        spacing="3",
    )
