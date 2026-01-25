# 06 - Notifications

**Requirement**: Notification publisher for grid events  
**AG Grid Feature**: Reflex State + Jump to Row  
**Demo Route**: `/06-notifications`

> **Note**: The notification panel is a demo-only component. It is implemented in the demo app, not in the main `reflex_ag_grid` package. Use it as a reference for building your own notification system.

## Overview

A notification system that displays alerts about grid events and allows users to click notifications to navigate to the relevant row.

## Demo Implementation

The demo app shows a complete notification system in:
- `ag_grid_demo/components/notification_panel.py` - UI component
- `ag_grid_demo/state.py` - State with notification methods

## Features

| Feature | Description |
|---------|-------------|
| Notification panel | Sidebar showing recent notifications |
| Click to jump | Navigate to row on notification click |
| Notification types | Info, warning, error, success |
| Flash on jump | Highlights the target row |
| Clear button | Dismiss all notifications |

## Code Example

### State with Notifications

```python
import reflex as rx

class State(rx.State):
    notifications: list[dict] = []
    
    def add_notification(self, message: str, row_id: str, level: str = "info"):
        """Add a notification (keep last 5)."""
        self.notifications = [
            {"message": message, "row_id": row_id, "level": level}
        ] + self.notifications[:4]
    
    def clear_notifications(self):
        """Clear all notifications."""
        self.notifications = []
    
    def jump_to_row(self, row_id: str):
        """Jump to and flash a row. Tries multiple grids."""
        return rx.call_script(f"""
            (() => {{
                // Try multiple possible grid refs
                const gridIds = ['notifications_grid', 'my_grid'];
                for (const gridId of gridIds) {{
                    const gridRef = refs['ref_' + gridId];
                    if (gridRef && gridRef.current && gridRef.current.api) {{
                        const api = gridRef.current.api;
                        const node = api.getRowNode('{row_id}');
                        if (node) {{
                            api.ensureNodeVisible(node, 'middle');
                            api.flashCells({{rowNodes: [node]}});
                            return;
                        }}
                    }}
                }}
            }})()
        """)
```

### Notification Panel Component

```python
def notification_panel() -> rx.Component:
    def notification_item(n: rx.Var[dict]) -> rx.Component:
        return rx.card(
            rx.hstack(
                rx.badge(
                    n["level"],
                    color_scheme=rx.match(
                        n["level"],
                        ("warning", "orange"),
                        ("success", "green"),
                        ("error", "red"),
                        "blue",
                    ),
                ),
                rx.text(n["message"], size="2", flex="1"),
                rx.button(
                    "→",
                    size="1",
                    on_click=State.jump_to_row(n["row_id"]),
                ),
            ),
            size="1",
        )
    
    return rx.vstack(
        rx.hstack(
            rx.heading("Notifications", size="4"),
            rx.button("Clear", size="1", on_click=State.clear_notifications),
        ),
        rx.cond(
            State.notifications.length() > 0,
            rx.foreach(State.notifications, notification_item),
            rx.text("No notifications", color="gray"),
        ),
        width="300px",
        padding="2",
        border="1px solid var(--gray-5)",
        border_radius="8px",
    )
```

## Key Implementation Details

1. **Single-parameter `jump_to_row`**: Reflex `on_click` handlers can't have extra parameters due to event signature constraints
2. **Try multiple grids**: The `jump_to_row` function iterates over possible grid IDs to find the row
3. **Use `refs` pattern**: AG Grid refs are named `ref_{grid_id}` 
4. **Flash cells**: `api.flashCells()` provides visual feedback when jumping

## How to Implement

1. Add `notifications: list[dict]` to your state
2. Create `add_notification()` and `clear_notifications()` methods
3. Create `jump_to_row()` that uses `rx.call_script` to call AG Grid API
4. Create a notification panel component
5. Wire up the arrow button to call `jump_to_row(n["row_id"])`

## Related Documentation

- [04 - Jump & Highlight](04_jump_highlight.md)
- [AG Grid Flash Cells](https://www.ag-grid.com/javascript-data-grid/flashing-cells/)
