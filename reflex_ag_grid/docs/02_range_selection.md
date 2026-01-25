# 02 - Range Selection

**Requirement**: Bulk state changes on multiple cells via range selection  
**AG Grid Feature**: Enterprise `enableRangeSelection`  
**Demo Route**: `/02-range-selection`

## Overview

Range selection allows users to select a rectangular block of cells by clicking and dragging. This enables bulk operations on multiple cells simultaneously.

## AG Grid Features Used

| Feature | Description |
|---------|-------------|
| `enable_range_selection` | Enable range selection mode |
| `cell_selection` | Enable cell-level selection |
| `on_range_selection_changed` | Event when selection changes |

## Code Example

```python
from reflex_ag_grid import ag_grid

ag_grid(
    id="range_grid",
    row_data=state.data,
    column_defs=columns,
    # Enable range selection
    enable_range_selection=True,
    cell_selection=True,
    theme="quartz",
)
```

## Features

- **Click and drag** to select cell ranges
- **Shift+click** to extend selection
- **Ctrl+click** for multiple ranges
- **Copy range** with Ctrl+C

## How to Implement

1. Add `enable_range_selection=True` to your grid
2. Add `cell_selection=True` for single cell selection
3. Handle `on_range_selection_changed` for custom logic

## Related Documentation

- [AG Grid Range Selection](https://www.ag-grid.com/javascript-data-grid/range-selection/)
