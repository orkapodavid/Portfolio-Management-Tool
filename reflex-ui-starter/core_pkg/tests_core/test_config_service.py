"""Tests for ConfigService — core business logic for application configuration."""

import pytest
from core.services.config_service import ConfigService


@pytest.fixture
def service():
    """Fresh ConfigService instance for each test."""
    return ConfigService()


class TestGetConfig:
    def test_returns_dict(self, service):
        config = service.get_config()
        assert isinstance(config, dict)
        assert len(config) > 0

    def test_has_default_keys(self, service):
        config = service.get_config()
        # At minimum, the config should have some keys
        assert len(config) > 0


class TestUpdateConfig:
    def test_update_single_key(self, service):
        original = service.get_config()
        first_key = list(original.keys())[0]
        service.update_config(first_key, "new_test_value")
        updated = service.get_config()
        assert updated[first_key] == "new_test_value"

    def test_update_preserves_other_keys(self, service):
        original = service.get_config().copy()
        keys = list(original.keys())
        if len(keys) >= 2:
            service.update_config(keys[0], "changed")
            updated = service.get_config()
            assert updated[keys[1]] == original[keys[1]]


class TestResetToDefaults:
    def test_reset_restores_original(self, service):
        original = service.get_config().copy()
        first_key = list(original.keys())[0]
        service.update_config(first_key, "mutated_value")
        service.reset_to_defaults()
        restored = service.get_config()
        assert restored[first_key] == original[first_key]
