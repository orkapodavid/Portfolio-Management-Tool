# 10 - WebSocket

**Requirement**: Real-time data updates via WebSocket  
**AG Grid Feature**: Reflex State + Transaction API  
**Demo Route**: `/10-websocket`

## Overview

Real-time data streaming uses Reflex's native WebSocket connection to push updates from the server to the grid. Combined with AG Grid's cell change flash, updates are highly visible.

## Features

| Feature | Description |
|---------|-------------|
| Reflex State | Native WebSocket integration |
| `enable_cell_change_flash` | Visual feedback on updates |
| Transaction API | Efficient delta updates |

## Code Example

```python
import reflex as rx
from reflex_ag_grid import ag_grid

class State(rx.State):
    data: list[dict] = []
    streaming: bool = False
    
    async def update_prices(self):
        """Simulate real-time price updates."""
        while self.streaming:
            # Update prices randomly
            for row in self.data:
                row["price"] *= (1 + random.uniform(-0.01, 0.01))
            yield  # Push update to client
            await asyncio.sleep(1)

ag_grid(
    id="streaming_grid",
    row_data=State.data,
    column_defs=columns,
    enable_cell_change_flash=True,  # Flash on update
    theme="quartz",
)
```

## Toggle Streaming

```python
rx.switch(
    checked=State.streaming,
    on_change=State.update_prices,
)
```

## How to Implement

1. Store data in Reflex state
2. Update state in async function with `yield`
3. Add `enable_cell_change_flash=True` for visual feedback
4. Updates automatically push via WebSocket

## Related Documentation

- [Reflex State](https://reflex.dev/docs/state/)
- [03 - Cell Flash](03_cell_flash.md)
