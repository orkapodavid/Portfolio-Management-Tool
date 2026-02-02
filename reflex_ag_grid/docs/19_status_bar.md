# 19 - Status Bar

**Requirement**: Row counts and aggregations  
**AG Grid Feature**: Status Bar Panels (Enterprise)  
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
| `agTotalAndFilteredRowCountComponent` | Total and filtered in one |

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

## Panel Options

Each panel config supports:

| Option | Type | Description |
|--------|------|-------------|
| `statusPanel` | `string` | Panel component name |
| `align` | `"left" \| "center" \| "right"` | Panel alignment |
| `key` | `string` | Unique identifier |
| `statusPanelParams` | `object` | Custom params passed to panel |

## Aggregation Panel

The `agAggregationComponent` shows aggregations for selected cells (numeric columns only):
- **Sum**: Total of selected values
- **Average**: Mean of selected values  
- **Min/Max**: Minimum and maximum values
- **Count**: Number of selected cells

Select multiple cells with Shift/Ctrl+Click to see aggregations.

## Related Documentation

- [AG Grid Status Bar](https://www.ag-grid.com/react-data-grid/status-bar/)
