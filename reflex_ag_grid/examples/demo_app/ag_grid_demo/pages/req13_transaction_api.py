"""
13 - Transaction API Page - Demonstrates cell-by-cell updates.

Requirement 13: Cell-by-cell update
AG Grid Feature: applyTransaction() for delta updates
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_basic_columns
from ..components import nav_bar, status_badge


def transaction_api_page() -> rx.Component:
    """Transaction API demo page.

    Features:
    - Delta updates (only changed cells)
    - Add/remove/update individual rows
    - Performance optimized for large datasets
    - No full grid re-render
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("13 - Transaction API", size="6"),
        rx.text("Requirement 13: Cell-by-cell update"),
        rx.callout(
            "Transaction API allows delta updates without re-rendering the entire grid. "
            "Click buttons to add, update, or remove rows.",
            icon="info",
        ),
        rx.hstack(
            rx.button(
                "➕ Add Row",
                on_click=DemoState.add_row,
                color_scheme="green",
            ),
            rx.button(
                "🔄 Update Random",
                on_click=DemoState.simulate_price_update,
                color_scheme="blue",
            ),
            rx.button(
                "➖ Remove Last",
                on_click=DemoState.remove_last_row,
                color_scheme="red",
            ),
        ),
        status_badge(),
        ag_grid(
            id="transaction_api_grid",
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            row_id_key="id",
            enable_cell_change_flash=True,
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        rx.box(
            rx.heading("Transaction API Usage:", size="4"),
            rx.code_block(
                """// Add rows
api.applyTransaction({ add: [newRow] });

// Update rows  
api.applyTransaction({ update: [updatedRow] });

// Remove rows
api.applyTransaction({ remove: [rowToRemove] });""",
                language="javascript",
            ),
            padding="3",
            background="var(--gray-2)",
            border_radius="8px",
        ),
        padding="4",
        spacing="3",
    )
