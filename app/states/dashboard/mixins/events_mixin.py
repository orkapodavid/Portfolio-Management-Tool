"""
Events Mixin - State functionality for Events data

This Mixin provides all events-related state variables, computed vars,
and event handlers.

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
Pattern: State Mixin for code reuse
"""

import reflex as rx
from app.services import DatabaseService
from app.states.dashboard.types import (
    EventCalendarItem,
    EventStreamItem,
    ReverseInquiryItem,
)


class EventsMixin(rx.State, mixin=True):
    """
    Mixin providing events data state and filtering.

    Data provided:
    - Event calendar
    - Event stream
    - Reverse inquiry
    """

    # Events data lists
    event_calendar: list[EventCalendarItem] = []
    event_stream: list[EventStreamItem] = []
    reverse_inquiry: list[ReverseInquiryItem] = []

    async def load_events_data(self):
        """Load all events data from DatabaseService."""
        try:
            service = DatabaseService()
            self.event_calendar = await service.get_event_calendar()
            self.event_stream = await service.get_event_stream()
            self.reverse_inquiry = await service.get_reverse_inquiry()
        except Exception as e:
            import logging

            logging.exception(f"Error loading events data: {e}")
