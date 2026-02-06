"""
Notification Constants

Enums and TypedDicts for type-safe notification handling.
Centralizes all notification-related constants to reduce duplication
and improve type checking across services and UI components.
"""

from enum import StrEnum
from typing import TypedDict


class NotificationCategory(StrEnum):
    """Categories for raw notifications from service providers.

    Used in service files when creating notification dictionaries.
    """

    ALERTS = "Alerts"
    PORTFOLIO = "Portfolio"
    NEWS = "News"
    SYSTEM = "System"


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


class RawNotification(TypedDict, total=False):
    """Schema for notifications from service providers.

    This is the format returned by provider functions registered
    with NotificationRegistry.
    """

    id: str
    category: str  # NotificationCategory value
    title: str
    message: str
    time_ago: str
    is_read: bool
    icon: str  # NotificationIcon value
    color: str  # NotificationColor value
    module: str
    subtab: str
    row_id: str
    grid_id: str
    ticker: str
