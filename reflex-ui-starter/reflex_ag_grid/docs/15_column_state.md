# Requirement 15: Save Table Format (Full Grid State)

Save and restore complete grid state including column widths, order, visibility, filters, and sorting.

## Implementation

Uses AG Grid's `getState()`/`setState()` API via client-side JavaScript + localStorage.

### JavaScript Setup

```javascript
// Helper to get AG Grid API from React Fiber
function getGridApi() {
    const wrapper = document.querySelector('.ag-root-wrapper');
    if (!wrapper) return null;
    
    const key = Object.keys(wrapper).find(k => k.startsWith('__reactFiber'));
    if (!key) return null;
    
    let fiber = wrapper[key];
    let maxDepth = 50;
    while (fiber && maxDepth-- > 0) {
        if (fiber.stateNode?.api?.getState) return fiber.stateNode.api;
        if (fiber.memoizedProps?.gridRef?.current?.api?.getState) {
            return fiber.memoizedProps.gridRef.current.api;
        }
        fiber = fiber.return;
    }
    return null;
}

// Save complete grid state
function saveGridState() {
    const api = getGridApi();
    if (api) {
        const state = api.getState();
        localStorage.setItem('gridState', JSON.stringify(state));
    }
}

// Restore complete grid state
function restoreGridState() {
    const api = getGridApi();
    const stateStr = localStorage.getItem('gridState');
    if (api && stateStr) {
        const state = JSON.parse(stateStr);
        // Remove flex property so saved widths apply
        if (state.column?.columns) {
            state.column.columns = state.column.columns.map(col => {
                const newCol = {...col};
                delete newCol.flex;
                return newCol;
            });
        }
        api.setState(state);
    }
}

// Reset to defaults
function resetGridState() {
    const api = getGridApi();
    if (api) {
        api.resetColumnState();
        api.setFilterModel(null);
        localStorage.removeItem('gridState');
    }
}
```

### Auto-Restore on Page Load

> [!TIP]
> In Reflex SPAs, use `setInterval` instead of `DOMContentLoaded`:

```javascript
(function() {
    let attempts = 0;
    const tryRestore = setInterval(() => {
        attempts++;
        const api = getGridApi();
        const stateStr = localStorage.getItem('gridState');
        
        if (api && stateStr) {
            clearInterval(tryRestore);
            setTimeout(() => {
                const state = JSON.parse(stateStr);
                if (state.column?.columns) {
                    state.column.columns = state.column.columns.map(col => {
                        const newCol = {...col};
                        delete newCol.flex;
                        return newCol;
                    });
                }
                api.setState(state);
            }, 100);
        } else if (attempts >= 30) clearInterval(tryRestore);
    }, 500);
})();
```

## What Gets Saved

| Category | State Saved |
|----------|-------------|
| **Columns** | Width, order, visibility, pinning |
| **Filters** | All column filter configurations |
| **Sorting** | Sort column and direction |

## Key Points

> [!IMPORTANT]
> **Remove `flex` property** when restoring - otherwise flex columns override saved widths.

- **Single API call**: `getState()` captures everything, `setState()` restores everything
- **Auto-restore**: Uses polling to wait for grid ready in SPAs
- **localStorage**: Persists across page refreshes and browser sessions

## Usage in Reflex

```python
rx.button("Save", on_click=rx.call_script("saveGridState()"))
rx.button("Restore", on_click=rx.call_script("restoreGridState()"))
rx.button("Reset", on_click=rx.call_script("resetGridState()"))
```

## Demo

See `examples/demo_app/ag_grid_demo/pages/req15_column_state.py`
