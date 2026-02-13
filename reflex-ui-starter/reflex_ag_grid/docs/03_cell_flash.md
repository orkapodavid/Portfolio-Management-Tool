# 03 - Cell Flash

**Requirement**: Blinking cell changes to highlight updates  
**AG Grid Feature**: `enableCellChangeFlash` and `api.flashCells()`  
**Demo Route**: `/03-cell-flash`

## Overview

Cell flashing provides visual feedback when cell values change. This is essential for real-time data applications like trading grids where users need to notice value changes immediately.

## AG Grid Features Used

| Feature | Description |
|---------|-------------|
| `enable_cell_change_flash` | Auto-flash on value changes |
| `api.flashCells()` | Programmatic cell flash |
| CSS classes | `ag-cell-data-changed`, `ag-cell-data-changed-animation` |

## Code Example

```python
from reflex_ag_grid import ag_grid

ag_grid(
    id="flash_grid",
    row_data=state.data,
    column_defs=columns,
    # Enable automatic cell flash on data changes
    enable_cell_change_flash=True,
    theme="quartz",
)
```

## Programmatic Flash

To flash specific cells via JavaScript:

```javascript
gridApi.flashCells({
    rowNodes: [rowNode],
    columns: ['price'],
    flashDelay: 200,
    fadeDelay: 500
});
```

## Customizing Flash Style

Override CSS for custom flash colors:

```css
.ag-cell-data-changed {
    background-color: yellow !important;
}
```

## How to Implement

1. Add `enable_cell_change_flash=True` to your grid
2. When data updates, changed cells will briefly flash
3. For manual control, use `api.flashCells()` via `rx.call_script`

## Related Documentation

- [AG Grid Flashing Cells](https://www.ag-grid.com/javascript-data-grid/flashing-cells/)
