"""
Notification Config Service — Core business logic for notification preferences.

Provides mock notification preferences for the starter template.
Replace with real persistence in production.
"""

from typing import Dict, List, Any


class NotificationConfigService:
    """Service for notification preference operations."""

    def __init__(self):
        self._preferences: Dict[str, bool] = {
            # Channels
            "in_app": True,
            "email": False,
            "push": False,
            # Categories
            "price_alerts": True,
            "volume_spikes": True,
            "risk_warnings": True,
            "news_earnings": False,
            "system_updates": True,
        }
        self._quiet_hours: Dict[str, Any] = {
            "enabled": False,
            "from": "22:00",
            "to": "07:00",
        }

    def get_preferences(self) -> Dict[str, bool]:
        """Get all notification preferences."""
        return dict(self._preferences)

    def get_quiet_hours(self) -> Dict[str, Any]:
        """Get quiet hours configuration."""
        return dict(self._quiet_hours)

    def update_preference(self, key: str, value: bool) -> Dict[str, bool]:
        """Update a single notification preference."""
        if key in self._preferences:
            self._preferences[key] = value
        return self.get_preferences()

    def update_quiet_hours(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update quiet hours settings."""
        self._quiet_hours.update(updates)
        return self.get_quiet_hours()

    def get_enabled_channels(self) -> List[str]:
        """Get list of enabled notification channels."""
        channels = ["in_app", "email", "push"]
        return [ch for ch in channels if self._preferences.get(ch, False)]

    def get_enabled_categories(self) -> List[str]:
        """Get list of enabled notification categories."""
        categories = ["price_alerts", "volume_spikes", "risk_warnings", "news_earnings", "system_updates"]
        return [cat for cat in categories if self._preferences.get(cat, False)]
