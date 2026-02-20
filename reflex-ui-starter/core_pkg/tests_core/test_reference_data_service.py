"""Tests for ReferenceDataService — core business logic for instrument reference data."""

import pytest
from core.services.reference_data_service import ReferenceDataService


@pytest.fixture
def service():
    """Fresh ReferenceDataService instance for each test."""
    return ReferenceDataService()


class TestGetReferenceData:
    def test_returns_list(self, service):
        data = service.get_reference_data()
        assert isinstance(data, list)
        assert len(data) == 12

    def test_rows_have_required_fields(self, service):
        data = service.get_reference_data()
        required = {"ticker", "name", "isin", "exchange", "currency", "industry", "country", "market_cap", "status"}
        for row in data:
            assert required.issubset(row.keys()), f"Missing keys for {row.get('ticker')}: {row.keys()}"

    def test_tickers_are_unique(self, service):
        data = service.get_reference_data()
        tickers = [r["ticker"] for r in data]
        assert len(tickers) == len(set(tickers)), "Duplicate tickers found"


class TestGetSummaryStats:
    def test_returns_dict(self, service):
        stats = service.get_summary_stats()
        assert isinstance(stats, dict)

    def test_has_required_keys(self, service):
        stats = service.get_summary_stats()
        required = {"total", "exchanges", "countries"}
        assert required.issubset(stats.keys())

    def test_total_matches_data_length(self, service):
        stats = service.get_summary_stats()
        data = service.get_reference_data()
        assert stats["total"] == len(data)
