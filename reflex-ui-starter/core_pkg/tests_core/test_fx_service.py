"""Tests for FxService — core business logic for FX data."""

import pytest
from core.services.fx_service import FxService


@pytest.fixture
def service():
    """Fresh FxService instance for each test."""
    return FxService()


class TestGetFxData:
    def test_returns_list(self, service):
        data = service.get_fx_data()
        assert isinstance(data, list)
        assert len(data) == 12

    def test_rows_have_required_fields(self, service):
        data = service.get_fx_data()
        required = {"pair", "bid", "ask", "mid", "spread", "change_pct", "volume", "session", "status"}
        for row in data:
            assert required.issubset(row.keys()), f"Missing keys for {row.get('pair')}: {row.keys()}"

    def test_ask_gt_bid(self, service):
        """Ask price should always be >= bid price (non-negative spread)."""
        data = service.get_fx_data()
        for row in data:
            assert row["ask"] >= row["bid"], f"Negative spread for {row['pair']}: bid={row['bid']}, ask={row['ask']}"


class TestGenerateTick:
    def test_preserves_row_count(self, service):
        data = service.get_fx_data()
        ticked = service.generate_tick(data)
        assert len(ticked) == len(data)

    def test_does_not_mutate_input(self, service):
        data = service.get_fx_data()
        original_first_mid = data[0]["mid"]
        service.generate_tick(data)
        # The original data should not be mutated
        assert data[0]["mid"] == original_first_mid

    def test_tick_maintains_ask_gt_bid(self, service):
        """After ticking, ask should still be >= bid."""
        data = service.get_fx_data()
        ticked = service.generate_tick(data)
        for row in ticked:
            assert row["ask"] >= row["bid"], f"Post-tick negative spread for {row['pair']}"

    def test_tick_preserves_pair_names(self, service):
        data = service.get_fx_data()
        ticked = service.generate_tick(data)
        original_pairs = {r["pair"] for r in data}
        ticked_pairs = {r["pair"] for r in ticked}
        assert original_pairs == ticked_pairs


class TestGetSummaryStats:
    def test_returns_dict(self, service):
        stats = service.get_summary_stats()
        assert isinstance(stats, dict)

    def test_has_required_keys(self, service):
        stats = service.get_summary_stats()
        required = {"total", "gainers", "losers"}
        assert required.issubset(stats.keys())
