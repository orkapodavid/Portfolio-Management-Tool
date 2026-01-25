"""
Demo App Components - Shared UI components.

Exports:
- nav_bar: Navigation bar for all pages
- status_badge: Shows last event status
- notification_panel: Notifications with jump-to-row
"""

from .nav_bar import nav_bar
from .notification_panel import notification_panel
from .status_badge import status_badge

__all__ = ["nav_bar", "notification_panel", "status_badge"]
