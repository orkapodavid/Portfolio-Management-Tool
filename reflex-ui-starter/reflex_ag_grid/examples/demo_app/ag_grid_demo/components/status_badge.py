"""
Status Badge Component - Shows last event status.
"""

import reflex as rx

from ..state import DemoState


def status_badge() -> rx.Component:
    """Status badge showing last event.

    Displays the most recent action/event in a blue badge.
    """
    return rx.badge(DemoState.last_event, color_scheme="blue")
