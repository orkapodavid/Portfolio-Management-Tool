"""
Event Calendar Mixin - Tab-specific state for Event Calendar data.

Provides auto-refresh background task and force refresh functionality.
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.services import DatabaseService
from app.states.events.types import EventCalendarItem


class EventCalendarMixin(rx.State, mixin=True):
    """
    Mixin providing Event Calendar data state with auto-refresh.
    """

    # Event Calendar data
    event_calendar: list[EventCalendarItem] = []
    is_loading_event_calendar: bool = False
    event_calendar_last_updated: str = "—"
    event_calendar_auto_refresh: bool = True

    async def load_event_calendar_data(self):
        """Load Event Calendar data from DatabaseService."""
        self.is_loading_event_calendar = True
        try:
            service = DatabaseService()
            self.event_calendar = await service.get_event_calendar()
            self.event_calendar_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error loading event calendar data: {e}")
        finally:
            self.is_loading_event_calendar = False

    @rx.event(background=True)
    async def start_event_calendar_auto_refresh(self):
        """Background task for Event Calendar auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.event_calendar_auto_refresh:
                    break
                self.simulate_event_calendar_update()
            await asyncio.sleep(2)

    def toggle_event_calendar_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.event_calendar_auto_refresh = value
        if value:
            return type(self).start_event_calendar_auto_refresh

    def simulate_event_calendar_update(self):
        """Simulated delta update for demo - random time changes."""
        if not self.event_calendar_auto_refresh or len(self.event_calendar) < 1:
            return

        import random

        # Create a new list to trigger change detection
        new_list = list(self.event_calendar)

        # Update 1-3 random rows
        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            # Create a new row dict (immutable update for AG Grid change detection)
            new_row = dict(old_row)

            # Simulate small time changes - update 'time' field
            if "time" in new_row and new_row["time"]:
                try:
                    # Parse and slightly adjust time
                    time_parts = new_row["time"].split(":")
                    if len(time_parts) >= 2:
                        hour = int(time_parts[0])
                        minute = int(time_parts[1].replace(" AM", "").replace(" PM", ""))
                        # Small random adjustment
                        minute = (minute + random.randint(-5, 5)) % 60
                        am_pm = "AM" if hour < 12 else "PM"
                        display_hour = hour if hour <= 12 else hour - 12
                        if display_hour == 0:
                            display_hour = 12
                        new_row["time"] = f"{display_hour}:{minute:02d} {am_pm}"
                except (ValueError, TypeError, IndexError):
                    pass

            new_list[idx] = new_row

        self.event_calendar = new_list
        self.event_calendar_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_event_calendar(self):
        """Force refresh event calendar data with loading overlay."""
        if self.is_loading_event_calendar:
            return  # Debounce
        self.is_loading_event_calendar = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.3)
        try:
            service = DatabaseService()
            self.event_calendar = await service.get_event_calendar()
            self.event_calendar_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing event calendar: {e}")
        finally:
            self.is_loading_event_calendar = False
