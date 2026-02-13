"""
Notification Type Definitions

TypedDict definitions for notification-related data structures.
Enhanced with navigation fields for jump-to-row.
"""

from typing import TypedDict


class NotificationItem(TypedDict):
    """Type definition for a notification item displayed in the sidebar."""

    id: str
    header: str
    ticker: str
    timestamp: str
    instruction: str
    type: str  # "alert", "warning", "info"
    read: bool
    # Navigation fields for jump-to-row
    grid_id: str  # e.g. "market_data_grid"
    row_id: str  # e.g. "AAPL"
    route: str  # e.g. "/dashboard/analytics"
