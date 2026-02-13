"""
User Service — Core business logic for user management.

Provides mock user data for the starter template.
Replace with real data source in production.
"""

from typing import List, Optional
import uuid
from datetime import datetime, timedelta
import random


class UserItem:
    """User data structure."""

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class UserService:
    """Service for user data operations."""

    def __init__(self):
        self._users: List[dict] = []
        self._initialized = False

    def get_users(self) -> List[dict]:
        """Get all users."""
        if not self._initialized:
            self._generate_mock_data()
            self._initialized = True
        return self._users

    def get_by_id(self, user_id: str) -> Optional[dict]:
        """Get a user by ID."""
        return next((u for u in self.get_users() if u["id"] == user_id), None)

    def get_active_count(self) -> int:
        """Get count of active users."""
        return len([u for u in self.get_users() if u["status"] == "active"])

    def get_total_count(self) -> int:
        """Get total user count."""
        return len(self.get_users())

    def get_recent_activity(self) -> List[dict]:
        """Get recent user activity events."""
        activities = [
            {"type": "signup", "user": "Alice Chen", "detail": "User signup completed", "time": "2 min ago", "color": "green"},
            {"type": "order", "user": "Bob Smith", "detail": "New order processed", "time": "5 min ago", "color": "blue"},
            {"type": "alert", "user": "System", "detail": "System alert resolved", "time": "12 min ago", "color": "amber"},
            {"type": "login", "user": "Carol Davis", "detail": "Admin login from new device", "time": "18 min ago", "color": "purple"},
            {"type": "export", "user": "David Lee", "detail": "Data export completed", "time": "25 min ago", "color": "teal"},
        ]
        return activities

    def _generate_mock_data(self):
        """Generate mock user data."""
        roles = ["Admin", "Editor", "Viewer", "Analyst"]
        statuses = ["active", "active", "active", "inactive", "pending"]
        names = [
            "Alice Chen", "Bob Smith", "Carol Davis", "David Lee", "Eve Johnson",
            "Frank Wilson", "Grace Kim", "Henry Park", "Iris Wang", "Jack Brown",
            "Kate Moore", "Leo Garcia", "Mia Taylor", "Nathan Clark", "Olivia Adams",
        ]

        for i, name in enumerate(names):
            days_ago = random.randint(0, 365)
            self._users.append({
                "id": str(uuid.uuid4()),
                "name": name,
                "email": f"{name.lower().replace(' ', '.')}@example.com",
                "role": random.choice(roles),
                "status": random.choice(statuses),
                "last_login": (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M"),
                "created_at": (datetime.now() - timedelta(days=days_ago + 100)).strftime("%Y-%m-%d"),
            })
