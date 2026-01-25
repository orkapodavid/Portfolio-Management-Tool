# 12 - Edit Pause

**Requirement**: Pause auto-refresh while editing  
**AG Grid Feature**: Cell editing events + state flag  
**Demo Route**: `/12-edit-pause`

## Overview

When streaming real-time data, you may want to pause updates while a user is editing a cell to prevent data loss or confusion.

## AG Grid Features Used

| Feature | Description |
|---------|-------------|
| `on_cell_editing_started` | Detect edit start |
| `on_cell_editing_stopped` | Detect edit end |
| State flag | Pause streaming during edit |

## Code Example

```python
import reflex as rx
from reflex_ag_grid import ag_grid

class State(rx.State):
    data: list[dict] = []
    is_editing: bool = False
    
    def on_editing_started(self, row_index: int, field: str):
        self.is_editing = True
    
    def on_editing_stopped(self, row_index: int, field: str):
        self.is_editing = False
    
    async def stream_updates(self):
        while True:
            if not self.is_editing:  # Only update when not editing
                self.update_data()
                yield
            await asyncio.sleep(1)

ag_grid(
    id="edit_pause_grid",
    row_data=State.data,
    column_defs=columns,
    on_cell_editing_started=State.on_editing_started,
    on_cell_editing_stopped=State.on_editing_stopped,
)
```

## How to Implement

1. Add `is_editing` state flag
2. Handle `on_cell_editing_started` to set flag True
3. Handle `on_cell_editing_stopped` to set flag False
4. Check flag before applying updates

## Related Documentation

- [AG Grid Cell Editing Events](https://www.ag-grid.com/javascript-data-grid/cell-editing/)
