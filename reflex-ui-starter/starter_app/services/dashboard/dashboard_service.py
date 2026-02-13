"""
Dashboard Service — app-layer re-export.

Re-exports core UserService and AnalyticsService for use by Reflex state mixins.
"""

from core.services.user_service import UserService
from core.services.analytics_service import AnalyticsService

__all__ = ["UserService", "AnalyticsService"]
