"""
Notification Service for Portfolio Management Tool.

This service handles notification management including alerts, portfolio updates,
news, and system notifications.

It aggregates notifications from the NotificationRegistry, where domain services
register their notification providers.

IMPORTANT: Mock notification providers are now defined in their respective domain services:
- market_data_service.py: Market data and FX notifications
- pnl_service.py: P&L notifications
- risk_service.py: Risk notifications
- position_service.py: Position notifications
- This file: System notifications only
"""

import logging
from typing import Optional
import random

from app.ag_grid_constants import GridId
from app.services.notifications.notification_registry import NotificationRegistry
from app.services.notifications.notification_constants import (
    NotificationCategory,
    NotificationIcon,
    NotificationColor,
)

logger = logging.getLogger(__name__)


# === SYSTEM NOTIFICATION PROVIDER ===
# System notifications are infrastructure-related and stay in NotificationService
def _get_system_notifications() -> list[dict]:
    """Mock system notifications for maintenance, API status, etc."""
    return [
        {
            "id": "sys-001",
            "category": NotificationCategory.SYSTEM,
            "title": "System Maintenance",
            "message": "Scheduled maintenance tonight from 10pm-12am EST",
            "time_ago": "1 day ago",
            "is_read": True,
            "icon": NotificationIcon.SETTINGS,
            "color": NotificationColor.GRAY,
            "module": "Market Data",
            "subtab": "Market Data",
            "row_id": "GOOGL",
            "grid_id": GridId.MARKET_DATA,
            "ticker": "SYSTEM",
        },
        {
            "id": "sys-002",
            "category": NotificationCategory.SYSTEM,
            "title": "API Connected",
            "message": "Bloomberg API connection restored",
            "time_ago": "6 hours ago",
            "is_read": True,
            "icon": NotificationIcon.CHECK_CIRCLE,
            "color": NotificationColor.GREEN,
            "module": "Market Data",
            "subtab": "Market Data",
            "row_id": "AMZN",
            "grid_id": GridId.MARKET_DATA,
            "ticker": "API",
        },
    ]


# Register system provider
NotificationRegistry.register("system", _get_system_notifications)


class NotificationService:
    """
    Service for managing notifications.

    Aggregates notifications from all registered providers in NotificationRegistry.

    Notification types:
    - Alerts (price alerts, risk alerts)
    - Portfolio (dividend, trade confirmations)
    - News (market updates)
    - System (security, account changes)
    """

    def __init__(self):
        """Initialize notification service."""
        pass

    async def get_notifications(
        self,
        category: Optional[str] = None,
        unread_only: bool = False,
        limit: Optional[int] = None,
    ) -> list[dict]:
        """
        Get notifications, optionally filtered by category.

        Aggregates from all registered notification providers.

        Args:
            category: Filter by category ('Alerts', 'Portfolio', 'News', 'System')
            unread_only: Only return unread notifications
            limit: Maximum number of notifications to return

        Returns:
            List of notification dictionaries
        """
        # Aggregate from registry
        all_notifications = NotificationRegistry.get_all_notifications()

        logger.debug(
            f"Aggregated {len(all_notifications)} notifications from "
            f"{len(NotificationRegistry.get_provider_names())} providers"
        )

        # Apply category filter
        if category and category != "All":
            all_notifications = [
                n for n in all_notifications if n["category"] == category
            ]

        # Apply unread filter
        if unread_only:
            all_notifications = [n for n in all_notifications if not n["is_read"]]

        # Apply limit
        if limit:
            all_notifications = all_notifications[:limit]

        return all_notifications

    async def mark_as_read(self, notification_id: str) -> bool:
        """
        Mark a notification as read.

        Args:
            notification_id: Notification ID to mark as read

        Returns:
            bool: True if successful

        TODO: Update database to mark notification as read.
        """
        logger.info(f"Mock: Marking notification {notification_id} as read")
        return True

    async def mark_all_as_read(self, category: Optional[str] = None) -> int:
        """
        Mark all notifications as read.

        Args:
            category: Optional category filter

        Returns:
            int: Number of notifications marked as read

        TODO: Batch update database records.
        """
        logger.info(f"Mock: Marking all notifications as read (category: {category})")
        return 10  # Mock count

    async def delete_notification(self, notification_id: str) -> bool:
        """
        Delete a notification.

        Args:
            notification_id: Notification ID to delete

        Returns:
            bool: True if successful

        TODO: Delete from database.
        """
        logger.info(f"Mock: Deleting notification {notification_id}")
        return True

    async def delete_all(self, category: Optional[str] = None) -> int:
        """
        Delete all notifications.

        Args:
            category: Optional category filter

        Returns:
            int: Number of notifications deleted

        TODO: Batch delete from database.
        """
        logger.info(f"Mock: Deleting all notifications (category: {category})")
        return 10  # Mock count

    async def create_notification(
        self,
        category: str,
        title: str,
        message: str,
        icon: str = "bell",
        color: str = "text-blue-500",
        module: str = "Market Data",
        subtab: str = "Market Data",
        row_id: str = "",
        grid_id: str = GridId.MARKET_DATA,
    ) -> dict:
        """
        Create a new notification.

        Args:
            category: Notification category
            title: Notification title
            message: Notification message
            icon: Icon name
            color: Color class
            module: Target module for navigation
            subtab: Target subtab for navigation
            row_id: Row ID to highlight in grid
            grid_id: Grid ID to target (use GridId enum)

        Returns:
            Created notification dict

        TODO: Insert into database and potentially push to client via websocket.
        """
        logger.info(f"Mock: Creating notification - {title}")

        return {
            "id": str(random.randint(1000, 9999)),
            "category": category,
            "title": title,
            "message": message,
            "time_ago": "Just now",
            "is_read": False,
            "icon": icon,
            "color": color,
            "module": module,
            "subtab": subtab,
            "row_id": row_id,
            "grid_id": grid_id,
        }


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    async def test_notification_service():
        service = NotificationService()

        # Test get notifications
        notifications = await service.get_notifications()
        print(f"All notifications: {len(notifications)}")
        print(f"Providers: {NotificationRegistry.get_provider_names()}")

        # Test filtered notifications
        alerts = await service.get_notifications(category="Alerts")
        print(f"Alerts: {len(alerts)}")

        # Test unread only
        unread = await service.get_notifications(unread_only=True)
        print(f"Unread: {len(unread)}")

    import asyncio

    asyncio.run(test_notification_service())
