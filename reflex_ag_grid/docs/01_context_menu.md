# 01 - Context Menu

**Requirement**: Right-click context menu for grid operations  
**AG Grid Feature**: Enterprise `getContextMenuItems()` callback  
**Demo Route**: `/01-context-menu`

## Overview

AG Grid Enterprise provides a customizable context menu that appears on right-click. This enables quick access to common operations like copy, export, and custom actions.

## AG Grid Features Used

| Feature | Description |
|---------|-------------|
| `getContextMenuItems` | Callback to define menu items |
| Built-in actions | `copy`, `copyWithHeaders`, `export`, `separator` |
| Custom items | User-defined menu items with handlers |

## Code Example

```python
from reflex_ag_grid import ag_grid

ag_grid(
    id="context_menu_grid",
    row_data=state.data,
    column_defs=columns,
    # Context menu is enabled by default in Enterprise
    # Custom menu items can be added via JavaScript
    theme="quartz",
)
```

## Default Context Menu Items

The following items are available by default:
- **Copy** - Copy selected cells
- **Copy with Headers** - Copy cells with column headers
- **Export** - Export to CSV or Excel
- **Separator** - Visual divider between groups

## How to Implement

1. AG Grid Enterprise enables context menu by default
2. Right-click any cell to see the menu
3. For custom items, use `getContextMenuItems` callback via JavaScript

## Related Documentation

- [AG Grid Context Menu](https://www.ag-grid.com/javascript-data-grid/context-menu/)
