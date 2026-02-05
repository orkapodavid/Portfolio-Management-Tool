"""
Events State - Module-specific state for Events data

Handles all event-related data:
- Event Calendar
- Event Stream
- Reverse Inquiry
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.services import DatabaseService
from app.states.types import (
    EventCalendarItem,
    EventStreamItem,
    ReverseInquiryItem,
)


class EventsState(rx.State):
    """
    State management for events data.
    """

    # Data storage
    event_calendar: list[EventCalendarItem] = []
    event_stream: list[EventStreamItem] = []
    reverse_inquiry: list[ReverseInquiryItem] = []

    # Event Calendar loading state
    is_loading_event_calendar: bool = False
    event_calendar_last_updated: str = "—"

    # Event Stream loading state
    is_loading_event_stream: bool = False
    event_stream_last_updated: str = "—"

    # Reverse Inquiry loading state
    is_loading_reverse_inquiry: bool = False
    reverse_inquiry_last_updated: str = "—"

    # UI state
    is_loading: bool = False
    current_tab: str = "calendar"

    # Shared UI state for sorting
    sort_column: str = ""
    sort_direction: str = "asc"
    selected_row: int = -1

    async def on_load(self):
        """Called when Events view loads."""
        await self.load_events_data()

    async def load_events_data(self):
        """Load all events data from DatabaseService."""
        self.is_loading = True
        try:
            service = DatabaseService()
            self.event_calendar = await service.get_event_calendar()
            self.event_calendar_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            self.event_stream = await service.get_event_stream()
            self.event_stream_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            self.reverse_inquiry = await service.get_reverse_inquiry()
            self.reverse_inquiry_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error loading events data: {e}")
        finally:
            self.is_loading = False

    # =========================================================================
    # Event Calendar
    # =========================================================================

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

    # =========================================================================
    # Event Stream
    # =========================================================================

    async def force_refresh_event_stream(self):
        """Force refresh event stream data with loading overlay."""
        if self.is_loading_event_stream:
            return  # Debounce
        self.is_loading_event_stream = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.3)
        try:
            service = DatabaseService()
            self.event_stream = await service.get_event_stream()
            self.event_stream_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing event stream: {e}")
        finally:
            self.is_loading_event_stream = False

    # =========================================================================
    # Reverse Inquiry
    # =========================================================================

    async def force_refresh_reverse_inquiry(self):
        """Force refresh reverse inquiry data with loading overlay."""
        if self.is_loading_reverse_inquiry:
            return  # Debounce
        self.is_loading_reverse_inquiry = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.3)
        try:
            service = DatabaseService()
            self.reverse_inquiry = await service.get_reverse_inquiry()
            self.reverse_inquiry_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing reverse inquiry: {e}")
        finally:
            self.is_loading_reverse_inquiry = False

    # =========================================================================
    # UI State Methods
    # =========================================================================

    def set_current_tab(self, tab: str):
        """Switch between events tabs."""
        self.current_tab = tab

    def toggle_sort(self, column: str):
        """Toggle sort direction for a column."""
        if self.sort_column == column:
            self.sort_direction = "desc" if self.sort_direction == "asc" else "asc"
        else:
            self.sort_column = column
            self.sort_direction = "asc"

    def set_selected_row(self, row_id: int):
        """Set selected row ID."""
        self.selected_row = row_id
