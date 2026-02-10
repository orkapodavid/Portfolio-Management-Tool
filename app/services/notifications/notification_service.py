"""
Notification Service — app-layer re-export.

Re-exports the core NotificationService for backward compatibility.
"""

from pmt_core.services.notifications.notification_service import NotificationService  # noqa: F401

__all__ = ["NotificationService"]
