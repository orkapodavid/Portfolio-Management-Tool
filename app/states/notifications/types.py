"""
Notification Type Definitions

This module contains TypedDict definitions for notification-related data structures.
"""

from typing import TypedDict


class NotificationItem(TypedDict):
    """Type definition for a notification item displayed in the sidebar.

    This is the transformed format used by UI components,
    converted from RawNotification by NotificationSidebarState.
    """

    id: str  # String IDs like "pnl-001", "sys-002"
    header: str
    ticker: str
    timestamp: str
    instruction: str
    type: str  # NotificationType value: "alert", "warning", "info"
    read: bool
    # Navigation fields
    module: str
    subtab: str
    row_id: str
    grid_id: str
