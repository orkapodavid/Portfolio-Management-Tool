"""Tests for AnalyticsService — core business logic for analytics/market data."""

import pytest
from core.services.analytics_service import AnalyticsService


@pytest.fixture
def service():
    """Fresh AnalyticsService instance for each test."""
    return AnalyticsService()


class TestGetMarketData:
    def test_returns_list(self, service):
        data = service.get_market_data()
        assert isinstance(data, list)
        assert len(data) == 10

    def test_rows_have_required_fields(self, service):
        data = service.get_market_data()
        required = {"ticker", "company", "price", "change", "volume", "marketCap", "sector"}
        for row in data:
            assert required.issubset(row.keys()), f"Missing keys in {row.keys()}"

    def test_prices_are_positive(self, service):
        data = service.get_market_data()
        for row in data:
            assert float(row["price"]) > 0, f"Non-positive price for {row['ticker']}"


class TestGetSummaryStats:
    def test_returns_dict(self, service):
        stats = service.get_summary_stats()
        assert isinstance(stats, dict)

    def test_has_required_keys(self, service):
        stats = service.get_summary_stats()
        required = {"total", "gainers", "losers", "avg_change"}
        assert required.issubset(stats.keys())

    def test_gainers_plus_losers_lte_total(self, service):
        stats = service.get_summary_stats()
        assert stats["gainers"] + stats["losers"] <= stats["total"]


class TestGetColumnDefs:
    def test_returns_list(self, service):
        cols = service.get_column_defs()
        assert isinstance(cols, list)
        assert len(cols) == 7

    def test_column_defs_have_field(self, service):
        cols = service.get_column_defs()
        for col in cols:
            assert "field" in col, f"Column def missing 'field': {col}"
