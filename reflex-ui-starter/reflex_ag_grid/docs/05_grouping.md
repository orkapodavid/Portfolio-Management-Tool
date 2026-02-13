# 05 - Grouping & Summary

**Requirement**: Row grouping with aggregation (sum, avg, count)  
**AG Grid Feature**: Enterprise Row Grouping  
**Demo Route**: `/05-grouping`

## Overview

Row grouping allows organizing rows into hierarchical groups based on column values. Combined with aggregation functions, this enables summary calculations at each group level.

## AG Grid Features Used

| Feature | Description |
|---------|-------------|
| `row_group` | Column used for grouping |
| `agg_func` | Aggregation function (sum, avg, min, max, count) |
| `row_group_panel_show` | Show drag-drop grouping panel |
| `group_default_expanded` | Auto-expand groups (-1 = all) |
| `enable_row_group` | Enable drag-to-group for column |

## Code Example

```python
from reflex_ag_grid import ag_grid

columns = [
    ag_grid.column_def(
        field="sector",
        header_name="Sector",
        row_group=True,  # Group by this column
        hide=True,       # Hide from main grid
    ),
    ag_grid.column_def(
        field="price",
        header_name="Price",
        agg_func="avg",  # Show average in group rows
    ),
    ag_grid.column_def(
        field="qty",
        header_name="Quantity",
        agg_func="sum",  # Show sum in group rows
    ),
]

ag_grid(
    id="grouped_grid",
    row_data=state.data,
    column_defs=columns,
    row_group_panel_show="always",     # Show grouping panel
    group_default_expanded=-1,          # Expand all groups
    default_col_def={"enableRowGroup": True},  # Allow drag-to-group
    theme="quartz",
)
```

## Aggregation Functions

| Function | Description |
|----------|-------------|
| `sum` | Total of all values |
| `avg` | Average of values |
| `min` | Minimum value |
| `max` | Maximum value |
| `count` | Number of rows |

## Drag-Drop Grouping

Enable the row group panel to allow users to drag columns for grouping:

1. Set `row_group_panel_show="always"`
2. Set `default_col_def={"enableRowGroup": True}`
3. Users can drag column headers to the grouping panel

## Grand Total Pinning (v33.3+)

Pin a grand total row at the top or bottom of the grid:

```python
ag_grid(
    id="grouped_grid",
    row_data=state.data,
    column_defs=columns,
    grand_total_row="bottom",  # or "pinnedBottom", "top", "pinnedTop"
)
```

> [!NOTE]
> Requires aggregation functions to be set on columns.

## How to Implement

1. Add `row_group=True` to grouping column
2. Add `agg_func="sum"` (or avg, min, max) to value columns
3. Enable row group panel with `row_group_panel_show="always"`
4. Optionally add `grand_total_row="bottom"` for pinned totals

## Related Documentation

- [AG Grid Row Grouping](https://www.ag-grid.com/javascript-data-grid/grouping/)
- [AG Grid Aggregation](https://www.ag-grid.com/javascript-data-grid/aggregation/)
- [AG Grid Grand Total Row](https://www.ag-grid.com/javascript-data-grid/aggregation-total-rows/)

