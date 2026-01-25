"""
Editable Grid Page - Demonstrates cell editors, validation, and edit tracking.

Requirements:
- Req 7: Data validation
- Req 11: Different cell editors
- Req 12: Disable auto-refresh on edit
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_editable_columns
from ..data import EDITABLE_VALIDATION
from ..components import nav_bar, status_badge


def editable_page() -> rx.Component:
    """Editable Grid page with validation.

    Features:
    - Multiple cell editor types (text, select, number, checkbox)
    - Field-level validation with Pydantic
    - Automatic pause during editing
    - Edit state tracking
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("Editable Grid with Validation", size="6"),
        rx.text("Features: Different cell editors, Validation schema, Pause on edit"),
        rx.hstack(
            status_badge(),
            rx.cond(
                DemoState.is_editing,
                rx.badge("✏️ Editing", color_scheme="orange"),
                rx.badge("Ready", color_scheme="green"),
            ),
            rx.switch(
                checked=DemoState.pause_on_edit,
                on_change=DemoState.toggle_pause_on_edit,
            ),
            rx.text("Pause updates while editing"),
        ),
        rx.text(
            "Validation: Price (0-1M), Qty (1-10K), Change (-100 to 100%), Symbol (A-Z), Sector (enum)",
            color="gray",
            size="2",
        ),
        ag_grid(
            id="editable_grid",
            row_data=DemoState.data,
            column_defs=get_editable_columns(),
            validation_schema=EDITABLE_VALIDATION.to_js_config(),
            on_cell_value_changed=DemoState.on_cell_edit,
            on_cell_editing_started=DemoState.on_editing_started,
            on_cell_editing_stopped=DemoState.on_editing_stopped,
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        padding="4",
        spacing="3",
    )
