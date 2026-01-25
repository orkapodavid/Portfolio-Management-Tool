"""
Column State Page - Demonstrates save/restore column state to localStorage.

Requirements:
- Req 15: Save table format
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_basic_columns
from ..components import nav_bar


def column_state_page() -> rx.Component:
    """Column State page for persistence.

    Features:
    - Save column state to localStorage
    - Restore column state on demand
    - Reset columns to default
    - Persists width, order, visibility
    """
    grid_id = "column_state_grid"

    # JavaScript to find AG Grid API via React fiber tree
    get_api_js = """(function() {
        const wrapper = document.querySelector('.ag-root-wrapper');
        if (!wrapper) { alert('Grid not found'); return null; }
        const key = Object.keys(wrapper).find(k => k.startsWith('__reactFiber'));
        if (!key) { alert('React fiber not found'); return null; }
        let fiber = wrapper[key];
        while (fiber) {
            if (fiber.stateNode && fiber.stateNode.api) return fiber.stateNode.api;
            fiber = fiber.return;
        }
        alert('Grid API not found. Please wait and try again.');
        return null;
    })()"""

    return rx.vstack(
        nav_bar(),
        rx.heading("Column State Persistence", size="6"),
        rx.text("Features: Save/restore column widths, order, visibility"),
        rx.hstack(
            rx.button(
                "Save Column State",
                on_click=rx.call_script(
                    f"const api = {get_api_js}; "
                    "if (api) { "
                    "  const state = api.getColumnState(); "
                    "  localStorage.setItem('agGridColumnState', JSON.stringify(state)); "
                    "  alert('Column state saved! (' + state.length + ' columns)'); "
                    "}"
                ),
            ),
            rx.button(
                "Restore Column State",
                on_click=rx.call_script(
                    f"const api = {get_api_js}; "
                    "const state = localStorage.getItem('agGridColumnState'); "
                    "if (api && state) { "
                    "  api.applyColumnState({state: JSON.parse(state), applyOrder: true}); "
                    "  alert('Column state restored!'); "
                    "} else if (!state) { "
                    "  alert('No saved state found. Save first.'); "
                    "}"
                ),
            ),
            rx.button(
                "Reset Columns",
                on_click=rx.call_script(
                    f"const api = {get_api_js}; "
                    "if (api) { api.resetColumnState(); alert('Columns reset to default!'); }"
                ),
            ),
        ),
        ag_grid(
            id=grid_id,
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        rx.text(
            "Resize or reorder columns, then save. Refresh page and restore.",
            color="gray",
        ),
        padding="4",
        spacing="3",
    )
