# 18 - Performance Testing

**Requirement**: Large dataset stress test  
**AG Grid Feature**: Virtual Scrolling + Row Virtualization  
**Demo Route**: `/18-perf-test`

## Overview

AG Grid handles large datasets efficiently through virtual scrolling - only visible rows are rendered in the DOM.

## Key Benefits

| Feature | Benefit |
|---------|---------|
| Virtual Scrolling | Only visible rows rendered |
| Row Virtualization | Smooth scrolling for 10,000+ rows |
| Low Memory | Minimal DOM footprint |
| Fast Render | Quick initial load |

## Python Usage

```python
class PerfTestState(rx.State):
    data: list[dict] = []
    
    def generate_data(self):
        self.data = [
            {"id": f"row_{i}", "symbol": "AAPL", "price": 175.5}
            for i in range(10000)  # 10,000 rows
        ]

ag_grid(
    row_data=PerfTestState.data,
    column_defs=[...],
    row_id_key="id",  # Important for performance
)
```

## Performance Tips

1. Always set `row_id_key` for delta updates
2. Use `enable_cell_change_flash` sparingly on large grids
3. Avoid complex cell renderers on 10k+ grids

## Related Documentation

- [AG Grid Row Virtualization](https://www.ag-grid.com/javascript-data-grid/dom-virtualisation/)
