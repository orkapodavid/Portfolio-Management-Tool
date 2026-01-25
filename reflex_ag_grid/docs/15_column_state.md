# 15 - Column State

**Requirement**: Save and restore table layout  
**AG Grid Feature**: Column State API + localStorage  
**Demo Route**: `/15-column-state`

## Overview

Column state persistence allows users to customize column order, widths, visibility, and sorting, then save and restore that configuration.

## AG Grid Features Used

| Feature | Description |
|---------|-------------|
| `api.getColumnState()` | Get current column state |
| `api.applyColumnState()` | Apply saved state |
| `localStorage` | Browser storage for persistence |

## Code Example

```javascript
// Save column state
function saveColumnState(gridApi) {
    const state = gridApi.getColumnState();
    localStorage.setItem('columnState', JSON.stringify(state));
}

// Restore column state
function restoreColumnState(gridApi) {
    const savedState = localStorage.getItem('columnState');
    if (savedState) {
        gridApi.applyColumnState({
            state: JSON.parse(savedState),
            applyOrder: true
        });
    }
}
```

## Python Usage

```python
from reflex_ag_grid import ag_grid
import reflex as rx

ag_grid(
    id="stateful_grid",
    row_data=state.data,
    column_defs=columns,
    on_grid_ready=rx.Var(
        """(e) => {
            // Restore on load
            const saved = localStorage.getItem('gridColumnState');
            if (saved) {
                e.api.applyColumnState({state: JSON.parse(saved), applyOrder: true});
            }
        }"""
    ).to(rx.EventChain),
    on_column_moved=rx.Var(
        """(e) => {
            // Save on change
            const state = e.api.getColumnState();
            localStorage.setItem('gridColumnState', JSON.stringify(state));
        }"""
    ).to(rx.EventChain),
)
```

## What Gets Saved

- Column order
- Column widths
- Column visibility (hidden/shown)
- Sort state
- Filter state (optional)

## How to Implement

1. On grid ready, check localStorage and apply saved state
2. On column move/resize/sort, save state to localStorage
3. Optionally add Reset button to clear saved state

## Related Documentation

- [AG Grid Column State](https://www.ag-grid.com/javascript-data-grid/column-state/)
