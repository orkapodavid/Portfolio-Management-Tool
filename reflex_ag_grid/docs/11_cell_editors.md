# 11 - Cell Editors

**Requirement**: Different cell editors for different data types  
**AG Grid Feature**: Cell Editors  
**Demo Route**: `/11-cell-editors`

## Overview

AG Grid provides built-in cell editors for various data types including text, numbers, dropdowns, checkboxes, and dates.

## AG Grid Features Used

| Feature | Description |
|---------|-------------|
| `cell_editor` | Editor component type |
| `cell_editor_params` | Editor configuration |
| `editable` | Enable/disable editing |

## Available Editors

| Editor | Usage |
|--------|-------|
| `agTextCellEditor` | Free text input |
| `agNumberCellEditor` | Numeric input |
| `agSelectCellEditor` | Dropdown select |
| `agCheckboxCellEditor` | Boolean checkbox |
| `agDateCellEditor` | Date picker |
| `agLargeTextCellEditor` | Multi-line text |

## Code Example

```python
from reflex_ag_grid import ag_grid

columns = [
    ag_grid.column_def(
        field="company",
        editable=True,
        cell_editor="agTextCellEditor",
    ),
    ag_grid.column_def(
        field="sector",
        editable=True,
        cell_editor="agSelectCellEditor",
        cell_editor_params={"values": ["Tech", "Finance", "Healthcare"]},
    ),
    ag_grid.column_def(
        field="price",
        editable=True,
        cell_editor="agNumberCellEditor",
    ),
    ag_grid.column_def(
        field="active",
        editable=True,
        cell_editor="agCheckboxCellEditor",
        cell_renderer="agCheckboxCellRenderer",
    ),
]
```

## How to Implement

1. Set `editable=True` on the column
2. Choose `cell_editor` type
3. Configure with `cell_editor_params` if needed
4. Handle `on_cell_value_changed` for save logic

## Related Documentation

- [AG Grid Cell Editors](https://www.ag-grid.com/javascript-data-grid/cell-editors/)
