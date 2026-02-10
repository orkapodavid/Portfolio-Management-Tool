"""
Notification Registry — app-layer re-export.

Re-exports the core NotificationRegistry for backward compatibility.
All imports of NotificationRegistry from app.services.notifications
continue to work unchanged.
"""

from pmt_core.services.notifications.notification_registry import (  # noqa: F401
    NotificationRegistry,
    NotificationProvider,
)

__all__ = ["NotificationRegistry", "NotificationProvider"]
