"""
Event Stream Mixin - Tab-specific state for Event Stream data.

Provides auto-refresh background task and force refresh functionality.
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.services import EventStreamService
from app.states.events.types import EventStreamItem
import logging
import random

class EventStreamMixin(rx.State, mixin=True):
    """
    Mixin providing Event Stream data state with auto-refresh.
    """

    # Event Stream data
    event_stream: list[EventStreamItem] = []
    is_loading_event_stream: bool = False
    event_stream_last_updated: str = "—"
    event_stream_auto_refresh: bool = True

    async def load_event_stream_data(self):
        """Load Event Stream data from EventStreamService."""
        self.is_loading_event_stream = True
        try:
            service = EventStreamService()
            self.event_stream = await service.get_event_stream()
            self.event_stream_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error loading event stream data: {e}")
        finally:
            self.is_loading_event_stream = False

    @rx.event(background=True)
    async def start_event_stream_auto_refresh(self):
        """Background task for Event Stream auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.event_stream_auto_refresh:
                    break
                self.simulate_event_stream_update()
            await asyncio.sleep(2)

    def toggle_event_stream_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.event_stream_auto_refresh = value
        if value:
            return type(self).start_event_stream_auto_refresh

    def simulate_event_stream_update(self):
        """Simulated delta update for demo - random notes changes."""
        if not self.event_stream_auto_refresh or len(self.event_stream) < 1:
            return

        # Create a new list to trigger change detection
        new_list = list(self.event_stream)

        # Update 1-3 random rows
        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            # Create a new row dict (immutable update for AG Grid change detection)
            new_row = dict(old_row)

            # Simulate update to updated_time field
            new_row["updated_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            new_list[idx] = new_row

        self.event_stream = new_list
        self.event_stream_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_event_stream(self):
        """Force refresh event stream data with loading overlay."""
        if self.is_loading_event_stream:
            return  # Debounce
        self.is_loading_event_stream = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.3)
        try:
            service = EventStreamService()
            self.event_stream = await service.get_event_stream()
            self.event_stream_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error refreshing event stream: {e}")
        finally:
            self.is_loading_event_stream = False
