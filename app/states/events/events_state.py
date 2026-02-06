"""
Events State - Module-specific state for Events data

Composes all event-related tab mixins:
- Event Calendar
- Event Stream
- Reverse Inquiry
"""

import reflex as rx
from app.states.events.mixins import (
    EventCalendarMixin,
    EventStreamMixin,
    ReverseInquiryMixin,
)


class EventsState(
    EventCalendarMixin,
    EventStreamMixin,
    ReverseInquiryMixin,
    rx.State,
):
    """
    State management for events data.
    Composes all event tab mixins for unified interface.
    """

    # UI state
    current_tab: str = "calendar"

    # Shared UI state for sorting
    sort_column: str = ""
    sort_direction: str = "asc"
    selected_row: int = -1

    async def on_load(self):
        """Called when Events view loads."""
        await self.load_events_data()

    async def load_events_data(self):
        """Load all events data from mixins."""
        await self.load_event_calendar_data()
        await self.load_event_stream_data()
        await self.load_reverse_inquiry_data()

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
