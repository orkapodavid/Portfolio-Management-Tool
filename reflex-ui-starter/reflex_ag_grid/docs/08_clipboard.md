# 08 - Clipboard

**Requirement**: Copy cell values with/without headers, raw vs formatted  
**AG Grid Feature**: Enterprise Clipboard API  
**Demo Route**: `/08-clipboard`

## Overview

AG Grid's clipboard integration allows copying cells to clipboard. You can configure whether to copy raw values or formatted display values, and optionally include column headers.

## AG Grid Features Used

| Feature | Description |
|---------|-------------|
| `cell_selection` | Enable single cell selection |
| `enable_range_selection` | Enable multi-cell selection |
| `processCellForClipboard` | Transform value before copy |
| `copyHeadersToClipboard` | Include headers when copying |

## Code Example

```python
from reflex_ag_grid import ag_grid
import reflex as rx

columns = [
    ag_grid.column_def(
        field="price",
        header_name="Price",
        # Display with currency symbol
        value_formatter=rx.Var(
            "(params) => '$' + params.value.toFixed(2)"
        ).to(rx.EventChain),
    ),
    ag_grid.column_def(
        field="market_cap",
        header_name="Market Cap",
        # Display with abbreviation: $175bn
        value_formatter=rx.Var(
            """(params) => {
                const val = params.value;
                if (val >= 1e9) return '$' + (val / 1e9).toFixed(0) + 'bn';
                return '$' + val;
            }"""
        ).to(rx.EventChain),
    ),
]

ag_grid(
    id="clipboard_grid",
    row_data=state.data,
    column_defs=columns,
    cell_selection=True,
    enable_range_selection=True,
    # Copy raw values, not formatted
    on_grid_ready=rx.Var(
        """(e) => {
            e.api.setGridOption('processCellForClipboard', (params) => {
                return params.value;  // Raw value only
            });
        }"""
    ).to(rx.EventChain),
)
```

## Display vs Clipboard

| Display | Clipboard |
|---------|-----------|
| $175.50 | 175.5 |
| $2.8tn | 2800000000000 |
| 2.50% | 2.5 |

## How to Implement

1. Add `cell_selection=True` for single cell selection
2. Add `enable_range_selection=True` for range selection
3. Use `processCellForClipboard` to control copied value
4. Return `params.value` for raw, `params.formatValue()` for formatted

## Related Documentation

- [AG Grid Clipboard](https://www.ag-grid.com/javascript-data-grid/clipboard/)
