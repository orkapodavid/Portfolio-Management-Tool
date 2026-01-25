"""
14 - Background Tasks Page - Demonstrates scheduled background updates.

Requirement 14: Update timing
AG Grid Feature: Reflex background task scheduling
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_basic_columns
from ..components import nav_bar, status_badge


def background_tasks_page() -> rx.Component:
    """Background Tasks demo page.

    Features:
    - Scheduled background updates
    - Configurable update interval
    - Non-blocking UI updates
    - Task cancellation
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("14 - Background Tasks", size="6"),
        rx.text("Requirement 14: Update timing"),
        rx.callout(
            "Background tasks run on intervals without blocking the UI. "
            "Toggle streaming to see scheduled updates.",
            icon="info",
        ),
        rx.hstack(
            rx.cond(
                DemoState.is_streaming,
                rx.button(
                    "⏹️ Stop Tasks",
                    color_scheme="red",
                    on_click=DemoState.toggle_streaming,
                ),
                rx.button(
                    "▶️ Start Tasks",
                    color_scheme="green",
                    on_click=DemoState.toggle_streaming,
                ),
            ),
            rx.text("Interval: 2 seconds", color="gray"),
            rx.badge(
                rx.cond(DemoState.is_streaming, "RUNNING", "STOPPED"),
                color_scheme=rx.cond(DemoState.is_streaming, "green", "gray"),
            ),
        ),
        status_badge(),
        ag_grid(
            id="background_tasks_grid",
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            row_id_key="id",
            enable_cell_change_flash=True,
            theme="quartz",
            width="90vw",
            height="55vh",
        ),
        rx.cond(
            DemoState.is_streaming,
            rx.moment(interval=2000, on_change=DemoState.simulate_price_update),
            rx.fragment(),
        ),
        rx.box(
            rx.heading("Python Background Task:", size="4"),
            rx.code_block(
                """@rx.background
async def background_update(self):
    while self.is_streaming:
        async with self:
            self.simulate_price_update()
        await asyncio.sleep(2)""",
                language="python",
            ),
            padding="3",
            background="var(--gray-2)",
            border_radius="8px",
        ),
        padding="4",
        spacing="3",
    )
