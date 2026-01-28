# 19 - Status Bar

**Requirement**: Row counts and aggregations  
**AG Grid Feature**: Status Bar Panels  
**Demo Route**: `/19-status-bar`

## Overview

The status bar displays row counts, selection info, and aggregations at the bottom of the grid.

## Built-in Status Panels

| Panel | Description |
|-------|-------------|
| `agTotalRowCountComponent` | Total row count |
| `agFilteredRowCountComponent` | Filtered row count |
| `agSelectedRowCountComponent` | Selected row count |
| `agAggregationComponent` | Sum/Avg/Min/Max of selected cells |

## Python Usage

```python
ag_grid(
    row_data=State.data,
    column_defs=[...],
    status_bar={
        "statusPanels": [
            {"statusPanel": "agTotalRowCountComponent", "align": "left"},
            {"statusPanel": "agFilteredRowCountComponent", "align": "left"},
            {"statusPanel": "agSelectedRowCountComponent", "align": "center"},
            {"statusPanel": "agAggregationComponent", "align": "right"},
        ],
    },
)
```

## Related Documentation

- [AG Grid Status Bar](https://www.ag-grid.com/javascript-data-grid/status-bar/)
