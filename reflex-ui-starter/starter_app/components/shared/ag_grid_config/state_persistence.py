"""
Grid state persistence — client-side JS for saving/restoring grid state via localStorage.

Uses AG Grid's getState()/setState() API for complete state persistence
(column widths/order, filters, and sorting in one call).
"""


def grid_state_script(storage_key: str, grid_id: str = "") -> str:
    """
    Generate client-side JavaScript for full grid state persistence.

    This script provides:
    - getGridApi_{key}(): Helper to access AG Grid API from React Fiber
    - saveGridState_{key}(): Save complete grid state to localStorage
    - restoreGridState_{key}(): Restore state with flex removal fix
    - resetGridState_{key}(): Reset grid to defaults
    - Auto-restore on page load using polling (works in SPA)

    Args:
        storage_key: Unique localStorage key for this grid's state
        grid_id: Optional grid ID to target specific grid (prevents API bleeding in SPA)

    Returns:
        JavaScript code string to be used with rx.script()

    Usage:
        rx.script(grid_state_script("my_grid_state", "my_grid"))
    """
    # Sanitize key for use as JS function suffix (replace dashes with underscores)
    safe_key = storage_key.replace("-", "_")

    # Build selector: if grid_id provided, target specific grid; otherwise fallback to first
    if grid_id:
        selector = f"'#{grid_id} .ag-root-wrapper'"
        fallback_selector = "'.ag-root-wrapper'"
        wrapper_js = f"""
    // Try to find grid by ID first, then fallback to any grid
    let wrapper = document.querySelector({selector});
    if (!wrapper) {{
        wrapper = document.querySelector({fallback_selector});
    }}
    if (!wrapper) return null;"""
    else:
        wrapper_js = """
    const wrapper = document.querySelector('.ag-root-wrapper');
    if (!wrapper) return null;"""

    return f"""
// Grid State Management for {storage_key}
// Uses AG Grid's getState()/setState() API for complete state persistence

function getGridApi_{safe_key}() {{{wrapper_js}

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

function saveGridState_{safe_key}() {{
    const api = getGridApi_{safe_key}();
    if (api) {{
        const state = api.getState();
        localStorage.setItem('{storage_key}', JSON.stringify(state));
        const parts = [];
        if (state.column) parts.push('columns');
        if (state.filter) parts.push('filters');
        if (state.sort) parts.push('sort');
        console.log('Saved grid state:', parts.join(', '));
    }} else {{
        console.warn('Grid API not ready for save');
    }}
}}

function restoreGridState_{safe_key}() {{
    const api = getGridApi_{safe_key}();
    const stateStr = localStorage.getItem('{storage_key}');
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
            console.log('Restored grid state');
        }} catch (e) {{
            console.error('Restore failed:', e);
        }}
    }} else if (!stateStr) {{
        console.log('No saved state found');
    }}
}}

function resetGridState_{safe_key}() {{
    const api = getGridApi_{safe_key}();
    if (api) {{
        api.resetColumnState();
        api.setFilterModel(null);
        localStorage.removeItem('{storage_key}');
        console.log('Reset grid state');
    }}
}}

// Auto-restore on page load (polling for SPA)
(function() {{
    let attempts = 0;
    const maxAttempts = 30;

    const tryRestore = setInterval(() => {{
        attempts++;
        const api = getGridApi_{safe_key}();
        const stateStr = localStorage.getItem('{storage_key}');

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
