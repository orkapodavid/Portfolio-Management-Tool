# 04 - Jump & Highlight

**Requirement**: Navigate to and highlight specific rows from notifications  
**AG Grid Feature**: `api.ensureNodeVisible()` and `api.flashCells()`  
**Demo Route**: `/04-jump-highlight`

## Overview

Jump & Highlight enables programmatic navigation to specific rows in the grid, scrolling them into view and optionally highlighting them. This is commonly used for notification systems where clicking a notification scrolls to the relevant row.

## AG Grid Features Used

| Feature | Description |
|---------|-------------|
| `api.ensureNodeVisible()` | Scroll row into view |
| `api.flashCells()` | Highlight the row |
| `api.getRowNode()` | Get row by ID |

## Code Example

```python
from reflex_ag_grid import jump_to_row
import reflex as rx

def on_notification_click(grid_id: str, row_id: str):
    return jump_to_row(grid_id, row_id, flash=True)
```

## JavaScript Implementation

```javascript
// Get the row node
const rowNode = gridApi.getRowNode(rowId);
if (rowNode) {
    // Scroll to row
    gridApi.ensureNodeVisible(rowNode, 'middle');
    // Flash the row
    gridApi.flashCells({ rowNodes: [rowNode] });
}
```

## Features

- **Scroll to row** - Auto-scroll grid to show the target row
- **Flash highlight** - Briefly highlight the row
- **Cross-page navigation** - Navigate to different page, then highlight

## How to Implement

1. Import `jump_to_row` from `reflex_ag_grid`
2. Call `jump_to_row(grid_id, row_id, flash=True)` on notification click
3. Grid will scroll and flash the target row

## Related Documentation

- [AG Grid Row API](https://www.ag-grid.com/javascript-data-grid/row-object/)
