# 12 - Edit Pause

**Requirement**: Pause auto-refresh while editing with manual resume  
**AG Grid Feature**: Cell editing events + state flag  
**Demo Route**: `/12-edit-pause`

## Overview

When streaming real-time data, updates pause automatically when a user edits a cell. Updates remain paused until the user explicitly clicks Resume to prevent accidental data overwrites.

## AG Grid Features Used

| Feature | Description |
|---------|-------------|
| `on_cell_editing_started` | Detect edit start, set pause flag |
| `on_cell_editing_stopped` | Detect edit end (pause remains) |
| State flag | `pause_on_edit` controls streaming |
| Manual resume | User clicks Resume to continue |

## Code Example

```python
import reflex as rx
from reflex_ag_grid import ag_grid

class State(rx.State):
    data: list[dict] = []
    is_editing: bool = False
    pause_on_edit: bool = False  # Stays True until manual resume
    
    def on_editing_started(self, row_index: int, field: str):
        self.is_editing = True
        self.pause_on_edit = True  # Pause immediately
    
    def on_editing_stopped(self, row_index: int, field: str):
        self.is_editing = False
        # DON'T auto-resume: pause_on_edit stays True
    
    def resume_updates(self):
        """Manual resume after editing."""
        self.pause_on_edit = False
    
    def simulate_update(self):
        if self.pause_on_edit:
            return  # Skip update while paused
        self.update_data()

# Single button: Resume (when paused) / Stop (when streaming) / Start (when stopped)
rx.cond(
    State.pause_on_edit,
    rx.button("▶️ Resume Updates", on_click=State.resume_updates),
    rx.cond(
        State.is_streaming,
        rx.button("⏹️ Stop Updates", on_click=State.toggle_streaming),
        rx.button("▶️ Start Updates", on_click=State.toggle_streaming),
    ),
)

ag_grid(
    id="edit_pause_grid",
    row_data=State.data,
    column_defs=columns,
    on_cell_editing_started=State.on_editing_started,
    on_cell_editing_stopped=State.on_editing_stopped,
)
```

## How to Implement

1. Add `pause_on_edit` state flag (not just `is_editing`)
2. Handle `on_cell_editing_started` to set both flags
3. Handle `on_cell_editing_stopped` to clear `is_editing` only
4. Add `resume_updates` method to clear `pause_on_edit`
5. Check `pause_on_edit` flag before applying updates
6. Use single button with 3 states: Resume/Stop/Start

## Related Documentation

- [AG Grid Cell Editing Events](https://www.ag-grid.com/javascript-data-grid/cell-editing/)

