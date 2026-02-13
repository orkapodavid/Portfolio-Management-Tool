"""
Analytics Mixin — State mixin for the Dashboard Analytics tab.

Loads market data and column definitions from AnalyticsService.
"""

import reflex as rx
from starter_app.services import AnalyticsService
from starter_app.states.dashboard.types import MarketDataItem, SummaryStats

_analytics_service = AnalyticsService()


class AnalyticsMixin(rx.State, mixin=True):
    """Mixin providing Dashboard Analytics data state."""

    # AG Grid state
    column_defs: list[dict] = []
    row_data: list[MarketDataItem] = []
    is_loading_analytics: bool = False
    analytics_error: str = ""

    # Summary
    summary_stats: SummaryStats = {"total": 0, "gainers": 0, "losers": 0, "avg_change": 0.0}

    @rx.event
    def load_analytics_data(self):
        """Load analytics data from AnalyticsService."""
        self.is_loading_analytics = True
        self.analytics_error = ""
        try:
            self.column_defs = _analytics_service.get_column_defs()
            self.row_data = _analytics_service.get_market_data()
            self.summary_stats = _analytics_service.get_summary_stats()
        except Exception as e:
            self.analytics_error = str(e)
        finally:
            self.is_loading_analytics = False

    @rx.var(cache=True)
    def row_count(self) -> int:
        """Total number of market data rows."""
        return len(self.row_data)
