"""
Events State - Module-specific state for Events data

Handles all event-related data:
- Event Calendar
- Event Stream
- Reverse Inquiry
"""

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

    # UI state
    is_loading: bool = False
    current_search_query: str = ""
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
            self.event_stream = await service.get_event_stream()
            self.reverse_inquiry = await service.get_reverse_inquiry()
        except Exception as e:
            import logging

            logging.exception(f"Error loading events data: {e}")
        finally:
            self.is_loading = False

    def set_search_query(self, query: str):
        """Update search query for filtering."""
        self.current_search_query = query

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

    @rx.var(cache=True)
    def filtered_event_calendar(self) -> list[EventCalendarItem]:
        """Filtered event calendar based on search query."""
        if not self.current_search_query:
            return self.event_calendar

        query = self.current_search_query.lower()
        return [
            item
            for item in self.event_calendar
            if query in item.get("ticker", "").lower()
            or query in item.get("company", "").lower()
            or query in item.get("underlying", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_event_stream(self) -> list[EventStreamItem]:
        """Filtered event stream based on search query."""
        if not self.current_search_query:
            return self.event_stream

        query = self.current_search_query.lower()
        return [
            item
            for item in self.event_stream
            if query in item.get("symbol", "").lower()
            or query in item.get("subject", "").lower()
            or query in item.get("event_type", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_reverse_inquiry(self) -> list[ReverseInquiryItem]:
        """Filtered reverse inquiry based on search query."""
        if not self.current_search_query:
            return self.reverse_inquiry

        query = self.current_search_query.lower()
        return [
            item
            for item in self.reverse_inquiry
            if query in item.get("ticker", "").lower()
            or query in item.get("company", "").lower()
            or query in item.get("agent", "").lower()
        ]
