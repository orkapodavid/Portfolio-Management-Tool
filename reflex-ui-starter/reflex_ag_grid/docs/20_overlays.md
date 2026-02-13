# 20 - Overlays

**Requirement**: Loading and no-rows feedback  
**AG Grid Feature**: Loading/No-Rows Overlays  
**Demo Route**: `/20-overlays`

## Overview

Overlays provide visual feedback during async operations (loading) or when no data is available.

## Overlay Types

| Overlay | When Shown |
|---------|------------|
| Loading | While fetching data |
| No Rows | When `row_data` is empty |

## Python Usage

```python
class OverlayState(rx.State):
    data: list[dict] = []
    is_loading: bool = False
    
    async def load_data(self):
        self.is_loading = True
        yield
        # Fetch data...
        self.is_loading = False

ag_grid(
    row_data=OverlayState.data,
    loading=OverlayState.is_loading,
    overlay_loading_template="<span>Loading data...</span>",
    overlay_no_rows_template="<span>No rows to display</span>",
)
```

## Related Documentation

- [AG Grid Overlays](https://www.ag-grid.com/javascript-data-grid/overlays/)
