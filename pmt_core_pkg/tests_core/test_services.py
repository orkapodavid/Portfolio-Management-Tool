"""
Tests for pmt_core.services module.
"""

import pytest
from pmt_core.services import PricingService, ReportService


class TestPricingService:
    """Tests for PricingService."""

    def test_pricing_service_instantiation(self):
        """Test PricingService can be instantiated."""
        service = PricingService()
        assert service is not None

    def test_price_bond(self):
        """Test price_bond returns expected structure."""
        service = PricingService()
        result = service.price_bond(
            instrument_id="BOND001",
            face_value=1000.0,
            coupon_rate=0.05,
            maturity_date="2030-01-01",
        )
        assert "instrument_id" in result
        assert "price" in result
        assert "duration" in result
        assert result["instrument_id"] == "BOND001"

    def test_price_warrant(self):
        """Test price_warrant returns expected structure."""
        service = PricingService()
        result = service.price_warrant(
            instrument_id="WARRANT001",
            underlying_price=100.0,
            strike_price=110.0,
            expiry_date="2025-06-30",
            volatility=0.3,
            risk_free_rate=0.05,
        )
        assert "instrument_id" in result
        assert "price" in result
        assert "delta" in result
        assert "gamma" in result
        assert "vega" in result
        assert result["instrument_id"] == "WARRANT001"

    def test_calculate_greeks(self):
        """Test calculate_greeks returns Greek values."""
        service = PricingService()
        result = service.calculate_greeks(
            instrument_id="OPT001",
            instrument_type="option",
        )
        assert "delta" in result
        assert "gamma" in result
        assert "vega" in result
        assert "theta" in result

    def test_price_convertible_bond(self):
        """Test price_convertible_bond returns combined valuation."""
        service = PricingService()
        result = service.price_convertible_bond(
            instrument_id="CB001",
            face_value=1000.0,
            conversion_ratio=10.0,
            underlying_price=95.0,
        )
        assert "total_price" in result
        assert "bond_value" in result
        assert "option_value" in result
        assert "parity" in result


class TestReportService:
    """Tests for ReportService."""

    def test_report_service_instantiation(self):
        """Test ReportService can be instantiated."""
        service = ReportService()
        assert service is not None

    def test_extract_report_data(self):
        """Test extract_report_data returns list."""
        service = ReportService()
        result = service.extract_report_data(
            report_type="position_full",
            params={"position_date": "2026-01-17"},
        )
        assert isinstance(result, list)

    def test_merge_report_data(self):
        """Test merge_report_data performs left join."""
        service = ReportService()
        primary = [
            {"id": 1, "name": "A"},
            {"id": 2, "name": "B"},
        ]
        secondary = [
            {"id": 1, "value": 100},
            {"id": 3, "value": 300},
        ]
        result = service.merge_report_data(
            primary_data=primary,
            secondary_data=secondary,
            primary_key="id",
            secondary_key="id",
        )
        assert len(result) == 2
        assert result[0].get("value") == 100
        assert "value" not in result[1]

    def test_process_report_data(self):
        """Test process_report_data returns status."""
        service = ReportService()
        result = service.process_report_data(
            report_type="test",
            data=[{"id": 1}],
            action="upsert",
        )
        assert result["status"] == "success"
        assert result["records_processed"] == 1

    def test_get_report_config(self):
        """Test get_report_config returns config dict."""
        service = ReportService()
        result = service.get_report_config("position_full")
        assert "report_type" in result
        assert "report_name" in result
        assert result["report_type"] == "position_full"

    def test_cache_and_retrieve(self):
        """Test caching functionality."""
        service = ReportService()
        test_data = [{"id": 1, "value": "test"}]

        service.cache_report("test_report", test_data)
        cached = service.get_cached_report("test_report")

        assert cached == test_data

    def test_evaluate_rules(self):
        """Test evaluate_rules returns list."""
        service = ReportService()
        result = service.evaluate_rules(
            report_type="test",
            data=[{"id": 1}],
        )
        assert isinstance(result, list)
