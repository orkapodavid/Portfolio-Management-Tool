"""
Notification Type Definitions

This module contains TypedDict definitions for notification-related data structures.
"""

from typing import TypedDict


class NotificationItem(TypedDict):
    """Type definition for a notification item displayed in the sidebar."""
    id: int
    header: str
    ticker: str
    timestamp: str
    instruction: str
    type: str
    read: bool
