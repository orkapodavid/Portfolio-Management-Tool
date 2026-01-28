# 15 - Column State

**Requirement**: Save and restore table layout with AUTO-SAVE  
**AG Grid Feature**: Column State API + localStorage + Event Handlers  
**Demo Route**: `/15-column-state`

## Overview

Column state persistence allows users to customize column order, widths, visibility, and sorting. Changes are AUTO-SAVED using AG Grid event handlers.

## AG Grid Features Used

| Feature | Description |
|---------|-------------|
| `api.getColumnState()` | Get current column state |
| `api.applyColumnState()` | Apply saved state |
| `on_column_resized` | Auto-save on resize |
| `on_column_moved` | Auto-save on reorder |
| `on_sort_changed` | Auto-save on sort |
| `localStorage` | Browser storage for persistence |

## Auto-Save Implementation

```python
# Auto-save script (silent save to localStorage)
AUTO_SAVE_JS = """(function() {
    const api = getGridApi();  // Helper to get AG Grid API
    if (api) {
        const state = api.getColumnState();
        localStorage.setItem('columnState', JSON.stringify(state));
        console.log('Auto-saved column state');
    }
})()"""

ag_grid(
    id="column_state_grid",
    row_data=State.data,
    column_defs=columns,
    # Auto-save on any column change
    on_column_resized=rx.call_script(AUTO_SAVE_JS),
    on_column_moved=rx.call_script(AUTO_SAVE_JS),
    on_sort_changed=rx.call_script(AUTO_SAVE_JS),
    on_column_visible=rx.call_script(AUTO_SAVE_JS),
    on_column_pinned=rx.call_script(AUTO_SAVE_JS),
)
```

## What Gets Saved

- Column order
- Column widths
- Column visibility (hidden/shown)
- Sort state
- Pinned columns

## How to Implement

1. Create auto-save JavaScript that gets column state and saves to localStorage
2. Attach to column change events: resized, moved, sorted, visible, pinned
3. On page load, restore state via Restore button
4. Add Reset button to clear saved state

## Related Documentation

- [AG Grid Column State](https://www.ag-grid.com/javascript-data-grid/column-state/)

