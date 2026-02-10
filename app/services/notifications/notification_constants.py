"""
Notification Constants — UI-specific enums and mappings.

Re-exports core NotificationCategory for convenience.
Provides Lucide icon names, Tailwind color classes, and
UI display type mappings that are app-layer concerns.
"""

from enum import StrEnum

# Re-export core constants for backward compatibility
from pmt_core.services.notifications.notification_constants import (  # noqa: F401
    NotificationCategory,
    RawNotification,
)


class NotificationType(StrEnum):
    """UI display types for notification cards.

    Used in notification_sidebar.py for styling.
    """

    ALERT = "alert"
    WARNING = "warning"
    INFO = "info"


class NotificationIcon(StrEnum):
    """Standard Lucide icon names for notifications."""

    # General
    BELL = "bell"
    CHECK_CIRCLE = "check-circle"
    CIRCLE_X = "circle-x"

    # Alerts
    ALERT_TRIANGLE = "alert-triangle"
    SHIELD_ALERT = "shield-alert"

    # Financial
    DOLLAR_SIGN = "dollar-sign"
    WALLET = "wallet"
    TRENDING_UP = "trending-up"
    ARROW_UP_CIRCLE = "arrow-up-circle"

    # System
    SETTINGS = "settings"
    GLOBE = "globe"

    # Content
    NEWSPAPER = "newspaper"
    LAYERS = "layers"
    PLUS_CIRCLE = "plus-circle"


class NotificationColor(StrEnum):
    """Tailwind text color classes for notification icons."""

    RED = "text-red-500"
    AMBER = "text-amber-500"
    YELLOW = "text-yellow-500"
    ORANGE = "text-orange-500"
    GREEN = "text-green-500"
    EMERALD = "text-emerald-500"
    TEAL = "text-teal-500"
    BLUE = "text-blue-500"
    INDIGO = "text-indigo-500"
    PURPLE = "text-purple-500"
    GRAY = "text-gray-500"


# === Category to Type Mapping ===
# Used in NotificationSidebarState to transform raw categories to UI types
CATEGORY_TO_TYPE: dict[str, str] = {
    NotificationCategory.ALERTS: NotificationType.ALERT,
    NotificationCategory.PORTFOLIO: NotificationType.INFO,
    NotificationCategory.NEWS: NotificationType.INFO,
    NotificationCategory.SYSTEM: NotificationType.INFO,
}
