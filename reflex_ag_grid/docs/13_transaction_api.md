# 13 - Transaction API

**Requirement**: Efficient cell-by-cell updates  
**AG Grid Feature**: Transaction API  
**Demo Route**: `/13-transaction-api`

## Overview

For large datasets with frequent updates, the Transaction API allows updating specific rows without re-rendering the entire grid.

## AG Grid Features Used

| Feature | Description |
|---------|-------------|
| `api.applyTransaction()` | Add/update/remove rows |
| Row ID | Unique identifier for each row |
| `getRowId` | Function to return row ID |

## Code Example

```javascript
// Add rows
gridApi.applyTransaction({
    add: [{ id: 1, symbol: 'AAPL', price: 175.50 }]
});

// Update rows
gridApi.applyTransaction({
    update: [{ id: 1, price: 176.00 }]
});

// Remove rows
gridApi.applyTransaction({
    remove: [{ id: 1 }]
});
```

## Python Usage

```python
import reflex as rx

def update_row(grid_id: str, row_data: dict):
    return rx.call_script(
        f"refs['ref_{grid_id}'].current.api.applyTransaction({{update: [{row_data}]}})"
    )
```

## How to Implement

1. Ensure each row has a unique `id` field
2. Configure `getRowId` to return the ID
3. Use `applyTransaction()` for efficient updates

## Related Documentation

- [AG Grid Transactions](https://www.ag-grid.com/javascript-data-grid/data-update-transactions/)
