# 18 - Performance Testing

**Requirement**: Large dataset stress test with continuous CRUD  
**AG Grid Feature**: Virtual Scrolling + Row Virtualization  
**Demo Route**: `/18-perf-test`

## Overview

AG Grid handles large datasets efficiently through virtual scrolling - only visible rows are rendered. This page also demonstrates continuous random CRUD operations.

## Key Features

| Feature | Benefit |
|---------|---------|
| Virtual Scrolling | Only visible rows rendered |
| Row Virtualization | Smooth scrolling for 10,000+ rows |
| Continuous CRUD | Stress test with add/update/delete |
| Cell Flashing | Visual feedback on changes |

## Continuous CRUD Mode

When "Start CRUD" is clicked, the grid performs these operations every 200ms:

- **UPDATE**: 10-50 random cells modified
- **CREATE**: 1-3 new rows added (10% chance per tick)
- **DELETE**: 1-2 rows removed (5% chance per tick)

Statistics are tracked and displayed in real-time badges.

## Python Usage

```python
class PerfTestState(rx.State):
    data: list[dict] = []
    is_running: bool = False
    update_count: int = 0
    rows_added: int = 0
    rows_deleted: int = 0
    cells_updated: int = 0
    
    def generate_data(self):
        self.data = [
            {"id": f"row_{i}", "symbol": "AAPL", "price": 175.5}
            for i in range(1000)
        ]
    
    def do_crud_tick(self):
        """Called by rx.interval - performs random CRUD."""
        if not self.is_running:
            return
        
        # Update random cells
        for _ in range(random.randint(10, 50)):
            idx = random.randint(0, len(self.data) - 1)
            self.data[idx]["price"] = round(random.uniform(50, 500), 2)
        
        # Add rows (10% chance)
        if random.random() < 0.1:
            self.data = self.data + [new_row]
        
        # Delete rows (5% chance)
        if random.random() < 0.05:
            self.data = self.data[:-1]

# Component with interval trigger
rx.cond(
    PerfTestState.is_running,
    rx.moment(interval=200, on_change=PerfTestState.do_crud_tick),
    rx.fragment(),
)

ag_grid(
    row_data=PerfTestState.data,
    row_id_key="id",  # Critical for performance
    enable_cell_change_flash=True,
)
```

## Performance Tips

1. Always set `row_id_key` for delta updates
2. Use `enable_cell_change_flash` to visualize changes
3. Avoid complex cell renderers on 10k+ grids
4. Use `rx.moment` interval instead of polling

## Related Documentation

- [AG Grid Row Virtualization](https://www.ag-grid.com/javascript-data-grid/dom-virtualisation/)
