# 14 - Background Tasks

**Requirement**: Scheduled update timing  
**AG Grid Feature**: Reflex Background Tasks  
**Demo Route**: `/14-background-tasks`

## Overview

Background tasks allow scheduling periodic updates without blocking the UI. This is essential for polling data sources or running cleanup tasks.

## Reflex Features Used

| Feature | Description |
|---------|-------------|
| `rx.background` | Decorator for background tasks |
| `yield` | Push updates to client |
| `asyncio.sleep()` | Delay between updates |

## Code Example

```python
import reflex as rx
import asyncio

class State(rx.State):
    data: list[dict] = []
    running: bool = False
    
    @rx.background
    async def periodic_refresh(self):
        self.running = True
        while self.running:
            async with self:
                await self.fetch_new_data()
            await asyncio.sleep(5)  # Update every 5 seconds
    
    async def fetch_new_data(self):
        # Fetch from API or database
        self.data = await get_latest_data()
    
    def stop_refresh(self):
        self.running = False
```

## Toggle Updates

```python
rx.switch(
    checked=State.running,
    on_change=lambda: State.periodic_refresh() if not State.running else State.stop_refresh(),
)
```

## How to Implement

1. Decorate async function with `@rx.background`
2. Use `async with self:` to access state
3. Use `await asyncio.sleep()` for timing
4. Toggle with boolean flag

## Related Documentation

- [Reflex Background Tasks](https://reflex.dev/docs/api-reference/background-tasks/)
