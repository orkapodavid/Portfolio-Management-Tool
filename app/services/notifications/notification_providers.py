"""
Notification Providers — app-layer wiring.

Imports core notification providers and registers them with the
NotificationRegistry at module load time. This module is imported
by app/services/__init__.py to ensure all providers are registered
at startup.
"""

from pmt_core.services.notifications.notification_registry import NotificationRegistry
from pmt_core.services.notifications.notification_providers import (
    get_pnl_notifications,
    get_position_notifications,
    get_risk_notifications,
    get_market_data_notifications,
    get_fx_notifications,
    get_system_notifications,
)


# === Register all core providers ===
NotificationRegistry.register("pnl", get_pnl_notifications)
NotificationRegistry.register("positions", get_position_notifications)
NotificationRegistry.register("risk", get_risk_notifications)
NotificationRegistry.register("market_data", get_market_data_notifications)
NotificationRegistry.register("fx", get_fx_notifications)
NotificationRegistry.register("system", get_system_notifications)
