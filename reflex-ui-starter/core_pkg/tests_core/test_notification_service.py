"""Tests for NotificationConfigService — core business logic for notification preferences."""

import pytest
from core.services.notification_service import NotificationConfigService


@pytest.fixture
def service():
    """Fresh NotificationConfigService instance for each test."""
    return NotificationConfigService()


class TestGetPreferences:
    def test_returns_dict(self, service):
        prefs = service.get_preferences()
        assert isinstance(prefs, dict)
        assert len(prefs) > 0


class TestUpdatePreference:
    def test_update_single_preference(self, service):
        prefs = service.get_preferences()
        first_key = list(prefs.keys())[0]
        original_value = prefs[first_key]
        new_value = not original_value if isinstance(original_value, bool) else "updated"
        service.update_preference(first_key, new_value)
        updated = service.get_preferences()
        assert updated[first_key] == new_value


class TestGetEnabledChannels:
    def test_returns_list(self, service):
        channels = service.get_enabled_channels()
        assert isinstance(channels, list)


class TestGetQuietHours:
    def test_returns_dict(self, service):
        quiet = service.get_quiet_hours()
        assert isinstance(quiet, dict)
