"""
12 - Edit Pause Page - Demonstrates disabling auto-refresh on edit + Undo/Redo.

Requirement 12: Disable auto-refresh on edit
AG Grid Feature: Edit tracking in State, undoRedoCellEditing
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
    - Undo/Redo cell editing (Phase 3)
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("12 - Edit Pause + Undo/Redo", size="6"),
        rx.text("Requirement 12: Disable auto-refresh on edit with Undo/Redo support"),
        rx.callout(
            "Start editing a cell while streaming is active. "
            "Updates will pause automatically. Use Undo/Redo to revert changes.",
            icon="info",
        ),
        rx.hstack(
            # Single button with 3 states: Resume (paused) > Stop (streaming) > Start (stopped)
            rx.cond(
                DemoState.pause_on_edit,
                # Paused - show Resume button
                rx.button(
                    "▶️ Resume Updates",
                    color_scheme="blue",
                    on_click=DemoState.resume_updates,
                ),
                # Not paused - show Start/Stop based on streaming state
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
            ),
            # Undo/Redo buttons (Phase 3)
            rx.button(
                "↩️ Undo",
                on_click=rx.call_script(
                    "refs['ref_edit_pause_grid']?.current?.api?.undoCellEditing()"
                ),
                color_scheme="gray",
                variant="outline",
            ),
            rx.button(
                "↪️ Redo",
                on_click=rx.call_script(
                    "refs['ref_edit_pause_grid']?.current?.api?.redoCellEditing()"
                ),
                color_scheme="gray",
                variant="outline",
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
            undo_redo_cell_editing=True,
            undo_redo_cell_editing_limit=20,
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
            "Undo/Redo: Ctrl+Z / Ctrl+Y or use buttons. Limit: 20 actions.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
