import reflex as rx
from typing import TypedDict
import datetime


class Notification(TypedDict):
    id: str
    category: str
    title: str
    message: str
    time_ago: str
    is_read: bool
    icon: str
    color: str


class NotificationState(rx.State):
    selected_category: str = "All"
    categories: list[str] = ["All", "Alerts", "Portfolio", "News", "System"]
    notifications: list[Notification] = [
        {
            "id": "1",
            "category": "Alerts",
            "title": "AAPL Price Alert",
            "message": "Apple Inc. has crossed above $190.00",
            "time_ago": "2 mins ago",
            "is_read": False,
            "icon": "bell",
            "color": "text-amber-500",
        },
        {
            "id": "2",
            "category": "Portfolio",
            "title": "Dividend Received",
            "message": "You received a dividend payment of $36.00 from AAPL",
            "time_ago": "2 hours ago",
            "is_read": False,
            "icon": "wallet",
            "color": "text-emerald-500",
        },
        {
            "id": "3",
            "category": "News",
            "title": "Market Update",
            "message": "Tech stocks rally as inflation data comes in lower than expected",
            "time_ago": "5 hours ago",
            "is_read": True,
            "icon": "newspaper",
            "color": "text-blue-500",
        },
        {
            "id": "4",
            "category": "System",
            "title": "Security Alert",
            "message": "New login detected from San Francisco, CA",
            "time_ago": "1 day ago",
            "is_read": True,
            "icon": "shield-alert",
            "color": "text-red-500",
        },
    ]

    @rx.var
    def filtered_notifications(self) -> list[Notification]:
        if self.selected_category == "All":
            return self.notifications
        return [
            n for n in self.notifications if n["category"] == self.selected_category
        ]

    @rx.var
    def unread_count(self) -> int:
        return len([n for n in self.notifications if not n["is_read"]])

    @rx.event
    def set_category(self, category: str):
        self.selected_category = category

    @rx.event
    def mark_all_read(self):
        new_notifications = []
        for n in self.notifications:
            n["is_read"] = True
            new_notifications.append(n)
        self.notifications = new_notifications
        rx.toast("All notifications marked as read", position="bottom-right")

    @rx.event
    def clear_all(self):
        self.notifications = []
        rx.toast("All notifications cleared", position="bottom-right")

    @rx.event
    def mark_read(self, notification_id: str):
        new_notifications = []
        for n in self.notifications:
            if n["id"] == notification_id:
                n["is_read"] = True
            new_notifications.append(n)
        self.notifications = new_notifications