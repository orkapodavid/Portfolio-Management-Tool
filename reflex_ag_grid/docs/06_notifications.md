# 06 - Notifications

**Requirement**: Notification publisher for grid events  
**AG Grid Feature**: Reflex State + Jump to Row  
**Demo Route**: `/06-notifications`

## Overview

A notification system that displays alerts about grid events and allows users to click notifications to navigate to the relevant row.

## Features

| Feature | Description |
|---------|-------------|
| Notification panel | Sidebar showing recent notifications |
| Click to jump | Navigate to row on notification click |
| Notification types | Info, warning, error, success |
| Auto-dismiss | Optional timeout for notifications |

## Code Example

```python
from reflex_ag_grid import notification_panel, jump_to_row
import reflex as rx

class State(rx.State):
    notifications: list[dict] = []
    
    def add_notification(self, message: str, row_id: str, level: str = "info"):
        self.notifications.append({
            "message": message,
            "row_id": row_id,
            "level": level,
        })
    
    def on_notification_click(self, row_id: str):
        return jump_to_row("my_grid", row_id, flash=True)
```

## Notification Panel Component

```python
notification_panel(
    notifications=State.notifications,
    on_click=State.on_notification_click,
    grid_id="my_grid",
)
```

## How to Implement

1. Store notifications in Reflex state
2. Use `notification_panel` component for UI
3. Handle click with `jump_to_row()` to navigate

## Related Documentation

- [04 - Jump & Highlight](04_jump_highlight.md)
