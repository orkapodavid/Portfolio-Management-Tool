"""
Notification Service for Portfolio Management Tool.

This service handles notification management including alerts, portfolio updates,
news, and system notifications.

TODO: Implement real notification logic with persistence.
"""

import logging
from typing import Optional
from datetime import datetime
import random

from app.ag_grid_constants import GridId

logger = logging.getLogger(__name__)


class NotificationService:
    """
    Service for managing notifications.
    
    Handles different notification types:
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
        limit: Optional[int] = None
    ) -> list[dict]:
        """
        Get notifications, optionally filtered by category.
        
        Args:
            category: Filter by category ('Alerts', 'Portfolio', 'News', 'System')
            unread_only: Only return unread notifications
            limit: Maximum number of notifications to return
            
        Returns:
            List of notification dictionaries
            
        TODO: Implement database query to fetch real notifications.
        """
        logger.warning("Using mock notification data.")
        
        # Mock notifications with navigation metadata
        # Using GridId enum for consistent grid targeting
        all_notifications = [
            # === MARKET DATA GRID NOTIFICATIONS ===
            {
                "id": "1",
                "category": "Alerts",
                "title": "Price Alert Triggered",
                "message": "TSLA has crossed above $200.00",
                "time_ago": "2 mins ago",
                "is_read": False,
                "icon": "bell",
                "color": "text-amber-500",
                "module": "Market Data",
                "subtab": "Market Data",
                "row_id": "TSLA",
                "grid_id": GridId.MARKET_DATA,
                "ticker": "TSLA",
            },
            {
                "id": "2",
                "category": "Portfolio",
                "title": "Trade Executed",
                "message": "Your order to buy 100 shares of AAPL has been filled at $189.50",
                "time_ago": "1 hour ago",
                "is_read": False,
                "icon": "wallet",
                "color": "text-emerald-500",
                "module": "Market Data",
                "subtab": "Market Data",
                "row_id": "AAPL",
                "grid_id": GridId.MARKET_DATA,
                "ticker": "AAPL",
            },
            {
                "id": "3",
                "category": "News",
                "title": "Market Update",
                "message": "S&P 500 reaches new all-time high amid strong earnings reports",
                "time_ago": "3 hours ago",
                "is_read": True,
                "icon": "newspaper",
                "color": "text-blue-500",
                "module": "Market Data",
                "subtab": "Market Data",
                "row_id": "MSFT",
                "grid_id": GridId.MARKET_DATA,
                "ticker": "MSFT",
            },
            {
                "id": "7",
                "category": "Alerts",
                "title": "Volume Spike",
                "message": "NVDA trading volume 3x average",
                "time_ago": "15 mins ago",
                "is_read": False,
                "icon": "trending-up",
                "color": "text-orange-500",
                "module": "Market Data",
                "subtab": "Market Data",
                "row_id": "NVDA",
                "grid_id": GridId.MARKET_DATA,
                "ticker": "NVDA",
            },
            {
                "id": "8",
                "category": "Alerts",
                "title": "52-Week High",
                "message": "GOOGL hit new 52-week high at $142.50",
                "time_ago": "30 mins ago",
                "is_read": False,
                "icon": "arrow-up-circle",
                "color": "text-green-500",
                "module": "Market Data",
                "subtab": "Market Data",
                "row_id": "GOOGL",
                "grid_id": GridId.MARKET_DATA,
                "ticker": "GOOGL",
            },
            # === POSITIONS GRID NOTIFICATIONS ===
            {
                "id": "9",
                "category": "Portfolio",
                "title": "Position Update",
                "message": "TKR0 position size updated after partial fill",
                "time_ago": "45 mins ago",
                "is_read": False,
                "icon": "layers",
                "color": "text-purple-500",
                "module": "Positions",
                "subtab": "Positions",
                "row_id": "TKR0",
                "grid_id": GridId.POSITIONS,
                "ticker": "TKR0",
            },
            {
                "id": "10",
                "category": "Portfolio",
                "title": "New Position",
                "message": "TKR5 added to portfolio",
                "time_ago": "2 hours ago",
                "is_read": True,
                "icon": "plus-circle",
                "color": "text-teal-500",
                "module": "Positions",
                "subtab": "Positions",
                "row_id": "TKR5",
                "grid_id": GridId.POSITIONS,
                "ticker": "TKR5",
            },
            # === PNL CHANGE GRID NOTIFICATIONS ===
            {
                "id": "11",
                "category": "Alerts",
                "title": "PnL Alert",
                "message": "AAPL daily PnL exceeded threshold",
                "time_ago": "10 mins ago",
                "is_read": False,
                "icon": "dollar-sign",
                "color": "text-yellow-500",
                "module": "PnL",
                "subtab": "PnL Change",
                "row_id": "AAPL",
                "grid_id": GridId.PNL_CHANGE,
                "ticker": "AAPL",
            },
            # === RISK GRID NOTIFICATIONS ===
            {
                "id": "4",
                "category": "Alerts",
                "title": "Risk Alert",
                "message": "Portfolio delta exposure has increased by 15%",
                "time_ago": "5 hours ago",
                "is_read": True,
                "icon": "alert-triangle",
                "color": "text-red-500",
                "module": "Risk",
                "subtab": "Delta Change",
                "row_id": "TSLA",  # Uses ticker as row_id_key
                "grid_id": GridId.DELTA_CHANGE,
                "ticker": "TSLA",
            },
            # === FX DATA GRID NOTIFICATIONS ===
            {
                "id": "12",
                "category": "News",
                "title": "FX Update",
                "message": "USD/JPY crossed 150 level",
                "time_ago": "20 mins ago",
                "is_read": False,
                "icon": "globe",
                "color": "text-indigo-500",
                "module": "Market Data",
                "subtab": "FX Data",
                "row_id": "USDJPY",  # Matches FX grid ticker format (no slash)
                "grid_id": GridId.FX_DATA,
                "ticker": "USD/JPY",  # Display name keeps slash
            },
            # === SYSTEM NOTIFICATIONS ===
            {
                "id": "5",
                "category": "System",
                "title": "System Maintenance",
                "message": "Scheduled maintenance tonight from 10pm-12am EST",
                "time_ago": "1 day ago",
                "is_read": True,
                "icon": "settings",
                "color": "text-gray-500",
                "module": "Market Data",
                "subtab": "Market Data",
                "row_id": "GOOGL",
                "grid_id": GridId.MARKET_DATA,
                "ticker": "SYSTEM",
            },
            {
                "id": "6",
                "category": "System",
                "title": "API Connected",
                "message": "Bloomberg API connection restored",
                "time_ago": "6 hours ago",
                "is_read": True,
                "icon": "check-circle",
                "color": "text-green-500",
                "module": "Market Data",
                "subtab": "Market Data",
                "row_id": "AMZN",
                "grid_id": GridId.MARKET_DATA,
                "ticker": "API",
            },
        ]
        
        # Apply category filter
        if category and category != "All":
            all_notifications = [n for n in all_notifications if n["category"] == category]
        
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
        
        # Test filtered notifications
        alerts = await service.get_notifications(category="Alerts")
        print(f"Alerts: {len(alerts)}")
        
        # Test unread only
        unread = await service.get_notifications(unread_only=True)
        print(f"Unread: {len(unread)}")
    
    import asyncio
    asyncio.run(test_notification_service())
