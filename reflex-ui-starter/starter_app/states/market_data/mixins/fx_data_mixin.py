"""
FX Data Mixin — State mixin for the Market Data FX Data tab.

Loads FX data from FxService and supports live ticking via background task.
"""

import asyncio

import reflex as rx
from starter_app.services import FxService

_fx_service = FxService()

# Tick interval in seconds
_TICK_INTERVAL = 1.5


class FxDataMixin(rx.State, mixin=True):
    """Mixin providing Market Data FX Data state with streaming support."""

    # AG Grid state
    fx_row_data: list[dict] = []
    is_loading_fx: bool = False
    fx_error: str = ""

    # Search
    fx_search_text: str = ""

    # Streaming
    fx_streaming: bool = False
    _fx_tick_guard: int = 0  # Guard against concurrent background tasks

    @rx.event
    def load_fx_data(self):
        """Load FX data from FxService."""
        self.is_loading_fx = True
        self.fx_error = ""
        try:
            self.fx_row_data = _fx_service.get_fx_data()
        except Exception as e:
            self.fx_error = str(e)
        finally:
            self.is_loading_fx = False

    @rx.event
    def toggle_fx_stream(self):
        """Toggle FX data streaming on/off."""
        self.fx_streaming = not self.fx_streaming
        if self.fx_streaming:
            return type(self).fx_tick_loop

    @rx.event
    def stop_fx_stream(self):
        """Explicitly stop streaming (e.g., on page leave)."""
        self.fx_streaming = False

    @rx.event(background=True)
    async def fx_tick_loop(self):
        """Background task that ticks FX data at regular intervals."""
        async with self:
            if self._fx_tick_guard > 0:
                return  # Already running
            self._fx_tick_guard += 1

        try:
            while True:
                async with self:
                    if not self.fx_streaming:
                        break
                    # Generate ticked data
                    self.fx_row_data = _fx_service.generate_tick(self.fx_row_data)

                await asyncio.sleep(_TICK_INTERVAL)
        finally:
            async with self:
                self._fx_tick_guard -= 1

    @rx.event
    def set_fx_search(self, value: str):
        self.fx_search_text = value

    @rx.event
    def clear_fx_search(self):
        self.fx_search_text = ""

    @rx.var(cache=True)
    def fx_row_count(self) -> int:
        """Total number of FX data rows."""
        return len(self.fx_row_data)
