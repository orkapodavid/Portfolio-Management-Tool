"""
03 - Cell Flash Page - Demonstrates blinking cell changes.

Requirement 3: Blinking cell changes
AG Grid Feature: api.flashCells()
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_basic_columns
from ..components import nav_bar


def cell_flash_page() -> rx.Component:
    """Cell Flash demo page.

    Features:
    - Cells flash when value changes
    - Visual feedback for updates
    - CSS animation on value change
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("03 - Cell Flash", size="6"),
        rx.text("Requirement 3: Blinking cell changes"),
        rx.callout(
            "Click 'Update Price' to see cells flash when values change.",
            icon="info",
        ),
        rx.hstack(
            rx.button(
                "Update Price",
                on_click=DemoState.simulate_price_update,
                color_scheme="blue",
            ),
            rx.text(f"Updates paused: ", color="gray"),
            rx.badge(
                rx.cond(DemoState.pause_on_edit, "Yes", "No"),
                color_scheme=rx.cond(DemoState.pause_on_edit, "orange", "green"),
            ),
        ),
        ag_grid(
            id="cell_flash_grid",
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            row_id_key="id",  # Critical for cell flash to work
            enable_cell_change_flash=True,
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        rx.text(
            "Cell flash uses CSS animation. Requires row_id_key for delta detection.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
