"""
15 - Column State Page - Demonstrates save/restore column state.

Requirement 15: Save table format
AG Grid Feature: localStorage column state persistence
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_basic_columns
from ..components import nav_bar


# JavaScript to access grid API
GET_API_JS = """(function() {
    const wrapper = document.querySelector('.ag-root-wrapper');
    if (!wrapper) { alert('Grid not found'); return null; }
    const key = Object.keys(wrapper).find(k => k.startsWith('__reactFiber'));
    if (!key) { alert('React fiber not found'); return null; }
    let fiber = wrapper[key];
    while (fiber) {
        if (fiber.stateNode && fiber.stateNode.api) return fiber.stateNode.api;
        fiber = fiber.return;
    }
    alert('Grid API not found');
    return null;
})()"""


def column_state_page() -> rx.Component:
    """Column State demo page.

    Features:
    - Save column state to localStorage
    - Restore column state on demand
    - Reset columns to default
    - Persists width, order, visibility, pinning
    """
    return rx.vstack(
        nav_bar(),
        rx.heading("15 - Column State", size="6"),
        rx.text("Requirement 15: Save table format"),
        rx.callout(
            "Resize, reorder, or hide columns, then save. "
            "Refresh the page and restore your layout.",
            icon="info",
        ),
        rx.hstack(
            rx.button(
                "💾 Save State",
                on_click=rx.call_script(
                    f"const api = {GET_API_JS}; "
                    "if (api) { "
                    "  const state = api.getColumnState(); "
                    "  localStorage.setItem('columnState15', JSON.stringify(state)); "
                    "  alert('Saved ' + state.length + ' columns'); "
                    "}"
                ),
                color_scheme="green",
            ),
            rx.button(
                "📂 Restore State",
                on_click=rx.call_script(
                    f"const api = {GET_API_JS}; "
                    "const state = localStorage.getItem('columnState15'); "
                    "if (api && state) { "
                    "  api.applyColumnState({state: JSON.parse(state), applyOrder: true}); "
                    "  alert('Restored!'); "
                    "} else if (!state) { alert('No saved state'); }"
                ),
                color_scheme="blue",
            ),
            rx.button(
                "🔄 Reset",
                on_click=rx.call_script(
                    f"const api = {GET_API_JS}; "
                    "if (api) { api.resetColumnState(); alert('Reset!'); }"
                ),
                color_scheme="gray",
            ),
        ),
        ag_grid(
            id="column_state_grid",
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        rx.text(
            "Column state includes: width, position, visibility, pinning, sorting.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
