"""
Notification Constants — UI-specific enums and mappings.

Provides Lucide icon names, Tailwind color classes, and
UI display type mappings.
"""

from enum import StrEnum


class NotificationType(StrEnum):
    """UI display types for notification cards."""

    ALERT = "alert"
    WARNING = "warning"
    INFO = "info"


class NotificationIcon(StrEnum):
    """Standard Lucide icon names for notifications."""

    BELL = "bell"
    CHECK_CIRCLE = "check-circle"
    CIRCLE_X = "circle-x"
    ALERT_TRIANGLE = "alert-triangle"
    SHIELD_ALERT = "shield-alert"
    DOLLAR_SIGN = "dollar-sign"
    TRENDING_UP = "trending-up"
    SETTINGS = "settings"
    NEWSPAPER = "newspaper"
    LAYERS = "layers"


class NotificationColor(StrEnum):
    """Tailwind text color classes for notification icons."""

    RED = "text-red-500"
    AMBER = "text-amber-500"
    YELLOW = "text-yellow-500"
    GREEN = "text-green-500"
    BLUE = "text-blue-500"
    PURPLE = "text-purple-500"
    GRAY = "text-gray-500"
