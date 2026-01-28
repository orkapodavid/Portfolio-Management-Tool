# 13 - Transaction API

**Requirement**: Efficient cell-by-cell updates  
**AG Grid Feature**: Transaction API + State Management  
**Demo Route**: `/13-transaction-api`

## Overview

For large datasets with frequent updates, use state methods to add/update/remove rows. AG Grid's `row_id_key` enables efficient delta updates.

## AG Grid Features Used

| Feature | Description |
|---------|-------------|
| `row_id_key` | Unique identifier for delta detection |
| State methods | `add_row()`, `remove_last_row()` |
| `enable_cell_change_flash` | Visual feedback on changes |

## Python State Methods

```python
class DemoState(rx.State):
    data: list[dict] = []
    
    def add_row(self):
        """Add a new row to the grid."""
        new_id = f"row_{len(self.data) + 1}"
        new_row = {
            "id": new_id,
            "symbol": "NEW",
            "company": "New Company",
            "price": 100.0,
        }
        self.data = self.data + [new_row]
    
    def remove_last_row(self):
        """Remove the last row from the grid."""
        if len(self.data) > 0:
            self.data = self.data[:-1]
    
    def simulate_price_update(self):
        """Update a random row's price."""
        idx = random.randint(0, len(self.data) - 1)
        self.data[idx]["price"] = round(self.data[idx]["price"] + random.uniform(-5, 5), 2)
```

## Grid Configuration

```python
ag_grid(
    id="transaction_api_grid",
    row_data=DemoState.data,
    column_defs=columns,
    row_id_key="id",  # Required for delta updates
    enable_cell_change_flash=True,  # Flash on change
)
```

## How to Implement

1. Add `row_id_key="id"` to grid for delta detection
2. Create state methods for add/update/remove operations
3. Connect buttons to state methods
4. Enable `cell_change_flash` for visual feedback

## Related Documentation

- [AG Grid Transactions](https://www.ag-grid.com/javascript-data-grid/data-update-transactions/)

