"""
Config Service — Core business logic for application configuration.

Provides mock configuration data for the starter template.
Replace with real persistence in production.
"""

from typing import Dict, Any, Optional


class ConfigService:
    """Service for application configuration operations."""

    def __init__(self):
        self._config: Dict[str, Any] = {
            "dark_mode": False,
            "compact_mode": True,
            "auto_refresh": True,
            "currency": "USD",
            "date_format": "us",
            "number_format": "us",
            "cache_duration": "15",
            "export_format": "csv",
        }

    def get_config(self) -> Dict[str, Any]:
        """Get all configuration values."""
        return dict(self._config)

    def get_value(self, key: str) -> Any:
        """Get a single config value."""
        return self._config.get(key)

    def update_config(self, key: str, value: Any) -> Dict[str, Any]:
        """Update a single config value."""
        self._config[key] = value
        return self.get_config()

    def update_many(self, updates: Dict[str, Any]) -> Dict[str, Any]:
        """Update multiple config values."""
        self._config.update(updates)
        return self.get_config()

    def reset_to_defaults(self) -> Dict[str, Any]:
        """Reset all configuration to defaults."""
        self.__init__()
        return self.get_config()
