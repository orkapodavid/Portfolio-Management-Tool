"""
12 - Edit Pause Page - Demonstrates disabling auto-refresh on edit.

Requirement 12: Disable auto-refresh on edit
AG Grid Feature: Edit tracking in State
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_editable_columns
from ..components import nav_bar, status_badge


def edit_pause_page() -> rx.Component:
    """Edit Pause demo page.

    Features:
    - Auto-pause updates when editing starts
    - Resume updates when editing stops
    - Visual indicator of edit state
    - Manual pause toggle
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("12 - Edit Pause", size="6"),
        rx.text("Requirement 12: Disable auto-refresh on edit"),
        rx.callout(
            "Start editing a cell while streaming is active. "
            "Updates will pause automatically until you finish editing.",
            icon="info",
        ),
        rx.hstack(
            rx.cond(
                DemoState.is_streaming,
                rx.button(
                    "⏹️ Stop Updates",
                    color_scheme="red",
                    on_click=DemoState.toggle_streaming,
                ),
                rx.button(
                    "▶️ Start Updates",
                    color_scheme="green",
                    on_click=DemoState.toggle_streaming,
                ),
            ),
            rx.text("Edit State:", weight="bold"),
            rx.cond(
                DemoState.is_editing,
                rx.badge("✏️ EDITING", color_scheme="orange"),
                rx.badge("Ready", color_scheme="green"),
            ),
            rx.text("Updates:", weight="bold"),
            rx.cond(
                DemoState.pause_on_edit,
                rx.badge("PAUSED", color_scheme="red"),
                rx.badge("ACTIVE", color_scheme="blue"),
            ),
            spacing="3",
        ),
        status_badge(),
        ag_grid(
            id="edit_pause_grid",
            row_data=DemoState.data,
            column_defs=get_editable_columns(),
            row_id_key="id",
            enable_cell_change_flash=True,
            on_cell_value_changed=DemoState.on_cell_edit,
            on_cell_editing_started=DemoState.on_editing_started,
            on_cell_editing_stopped=DemoState.on_editing_stopped,
            theme="quartz",
            width="90vw",
            height="55vh",
        ),
        rx.cond(
            DemoState.is_streaming,
            rx.moment(interval=2000, on_change=DemoState.simulate_price_update),
            rx.fragment(),
        ),
        rx.text(
            "on_cell_editing_started and on_cell_editing_stopped events track edit state.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
