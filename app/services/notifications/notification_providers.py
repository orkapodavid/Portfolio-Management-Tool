"""
Notification Providers for domain services.

Centralizes all mock notification provider functions and their
NotificationRegistry registrations. These were previously scattered
across individual service files (pnl, positions, risk, market_data).

This module is imported at app startup to ensure all providers are registered.
"""

from app.ag_grid_constants import GridId
from app.services.notifications.notification_registry import NotificationRegistry
from app.services.notifications.notification_constants import (
    NotificationCategory,
    NotificationIcon,
    NotificationColor,
)


# === PnL Notifications ===
def _get_pnl_notifications() -> list[dict]:
    """Mock PnL notifications for P&L threshold alerts."""
    return [
        {
            "id": "pnl-001",
            "category": NotificationCategory.ALERTS,
            "title": "PnL Alert",
            "message": "AAPL daily PnL exceeded threshold",
            "time_ago": "10 mins ago",
            "is_read": False,
            "icon": NotificationIcon.DOLLAR_SIGN,
            "color": NotificationColor.YELLOW,
            "module": "PnL",
            "subtab": "PnL Change",
            "row_id": "AAPL",
            "grid_id": GridId.PNL_CHANGE,
            "ticker": "AAPL",
        },
    ]


# === Position Notifications ===
def _get_position_notifications() -> list[dict]:
    """Mock position-related notifications."""
    return [
        {
            "id": "pos-001",
            "category": NotificationCategory.PORTFOLIO,
            "title": "Position Update",
            "message": "TKR0 position size updated after partial fill",
            "time_ago": "45 mins ago",
            "is_read": False,
            "icon": NotificationIcon.LAYERS,
            "color": NotificationColor.PURPLE,
            "module": "Positions",
            "subtab": "Positions",
            "row_id": "TKR0",
            "grid_id": GridId.POSITIONS,
            "ticker": "TKR0",
        },
        {
            "id": "pos-002",
            "category": NotificationCategory.PORTFOLIO,
            "title": "New Position",
            "message": "TKR5 added to portfolio",
            "time_ago": "2 hours ago",
            "is_read": True,
            "icon": NotificationIcon.PLUS_CIRCLE,
            "color": NotificationColor.TEAL,
            "module": "Positions",
            "subtab": "Positions",
            "row_id": "TKR5",
            "grid_id": GridId.POSITIONS,
            "ticker": "TKR5",
        },
    ]


# === Risk Notifications ===
def _get_risk_notifications() -> list[dict]:
    """Mock risk notifications for delta/gamma exposure alerts."""
    return [
        {
            "id": "risk-001",
            "category": NotificationCategory.ALERTS,
            "title": "Risk Alert",
            "message": "Portfolio delta exposure has increased by 15%",
            "time_ago": "5 hours ago",
            "is_read": True,
            "icon": NotificationIcon.ALERT_TRIANGLE,
            "color": NotificationColor.RED,
            "module": "Risk",
            "subtab": "Delta Change",
            "row_id": "TSLA",
            "grid_id": GridId.DELTA_CHANGE,
            "ticker": "TSLA",
        },
    ]


# === Register all providers ===
NotificationRegistry.register("pnl", _get_pnl_notifications)
NotificationRegistry.register("positions", _get_position_notifications)
NotificationRegistry.register("risk", _get_risk_notifications)
