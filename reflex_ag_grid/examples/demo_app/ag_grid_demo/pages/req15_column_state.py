"""
15 - Grid State Page - Demonstrates save/restore complete grid state.

Requirement 15: Save table format (columns, filters, sorting, etc.)
AG Grid Feature: Full Grid State API (getState/setState) + localStorage
"""

import reflex as rx

from reflex_ag_grid import ag_grid

from ..state import DemoState
from ..columns import get_basic_columns
from ..components import nav_bar


# Storage key for grid state
STORAGE_KEY = "gridState15"

# Client-side script for grid state management
# Uses getState()/setState() for complete grid state persistence
CLIENT_SIDE_SCRIPT = f"""
// Helper function to get AG Grid API from the DOM
function getGridApi() {{
    const wrapper = document.querySelector('.ag-root-wrapper');
    if (!wrapper) return null;
    
    const key = Object.keys(wrapper).find(k => k.startsWith('__reactFiber'));
    if (!key) return null;
    
    let fiber = wrapper[key];
    let maxDepth = 50;
    while (fiber && maxDepth-- > 0) {{
        if (fiber.stateNode && typeof fiber.stateNode.api === 'object' && fiber.stateNode.api !== null) {{
            if (typeof fiber.stateNode.api.getState === 'function') {{
                return fiber.stateNode.api;
            }}
        }}
        if (fiber.memoizedProps && fiber.memoizedProps.gridRef && fiber.memoizedProps.gridRef.current) {{
            const api = fiber.memoizedProps.gridRef.current.api;
            if (api && typeof api.getState === 'function') {{
                return api;
            }}
        }}
        fiber = fiber.return;
    }}
    return null;
}}

// Save complete grid state to localStorage
function saveGridState() {{
    const api = getGridApi();
    if (api) {{
        const state = api.getState();
        localStorage.setItem('{STORAGE_KEY}', JSON.stringify(state));
        const parts = [];
        if (state.column) parts.push('columns');
        if (state.filter) parts.push('filters');
        if (state.sort) parts.push('sort');
        alert('Saved: ' + parts.join(', '));
    }} else {{
        alert('Grid not ready');
    }}
}}

// Restore complete grid state from localStorage
function restoreGridState() {{
    const api = getGridApi();
    const stateStr = localStorage.getItem('{STORAGE_KEY}');
    if (api && stateStr) {{
        try {{
            const state = JSON.parse(stateStr);
            // Fix flex issue: remove flex from column state so widths apply
            if (state.column && state.column.columns) {{
                state.column.columns = state.column.columns.map(col => {{
                    const newCol = {{...col}};
                    delete newCol.flex;
                    return newCol;
                }});
            }}
            api.setState(state);
            alert('Restored!');
        }} catch (e) {{
            alert('Restore failed: ' + e.message);
        }}
    }} else if (!stateStr) {{
        alert('No saved state');
    }} else {{
        alert('Grid not ready');
    }}
}}

// Reset grid state (clear localStorage and reset grid)
function resetGridState() {{
    const api = getGridApi();
    if (api) {{
        api.resetColumnState();
        api.setFilterModel(null);
        localStorage.removeItem('{STORAGE_KEY}');
        alert('Reset!');
    }} else {{
        alert('Grid not ready');
    }}
}}

// Auto-restore on page load using immediate interval (works in SPA)
(function() {{
    let attempts = 0;
    const maxAttempts = 30;
    
    const tryRestore = setInterval(() => {{
        attempts++;
        const api = getGridApi();
        const stateStr = localStorage.getItem('{STORAGE_KEY}');
        
        if (api && stateStr) {{
            clearInterval(tryRestore);
            setTimeout(() => {{
                try {{
                    const state = JSON.parse(stateStr);
                    // Fix flex issue
                    if (state.column && state.column.columns) {{
                        state.column.columns = state.column.columns.map(col => {{
                            const newCol = {{...col}};
                            delete newCol.flex;
                            return newCol;
                        }});
                    }}
                    api.setState(state);
                    console.log('Auto-restored grid state after', attempts, 'attempts');
                }} catch (e) {{
                    console.error('Auto-restore failed:', e);
                }}
            }}, 100);
        }} else if (attempts >= maxAttempts) {{
            clearInterval(tryRestore);
        }}
    }}, 500);
}})();
"""


def column_state_page() -> rx.Component:
    """Grid State demo page.

    Features:
    - Auto-restore complete grid state on page load
    - Save full state (columns, filters, sort) to localStorage
    - Restore on demand
    - Reset to defaults
    """
    return rx.vstack(
        rx.script(CLIENT_SIDE_SCRIPT),
        nav_bar(),
        rx.heading("15 - Grid State", size="6"),
        rx.text("Requirement 15: Save table format (columns + filters + sort)"),
        rx.callout(
            "Grid state is AUTO-RESTORED on page load! "
            "Resize columns, apply filters, sort - then Save to persist everything.",
            icon="info",
        ),
        rx.hstack(
            rx.button(
                "💾 Save State",
                on_click=rx.call_script("saveGridState()"),
                color_scheme="green",
            ),
            rx.button(
                "📥 Restore State",
                on_click=rx.call_script("restoreGridState()"),
                color_scheme="blue",
            ),
            rx.button(
                "🔄 Reset",
                on_click=rx.call_script("resetGridState()"),
                color_scheme="gray",
            ),
        ),
        ag_grid(
            id="grid_state_demo",
            row_data=DemoState.data,
            column_defs=get_basic_columns(),
            row_id_key="id",
            theme="quartz",
            width="90vw",
            height="60vh",
        ),
        rx.text(
            "Full grid state: column widths/order/visibility, filters, and sort. "
            "Uses getState()/setState() API.",
            color="gray",
            size="2",
        ),
        padding="4",
        spacing="3",
    )
