"""
Core Performance Service for Portfolio Management Tool.

Provides KPI metrics and portfolio holdings data.
TODO: Replace mock data with repository calls.
"""

import logging

logger = logging.getLogger(__name__)


class PerformanceService:
    """Core service for performance header data (KPIs, holdings)."""

    async def get_kpi_metrics(self) -> list[dict]:
        """
        Get KPI metrics for the header cards.

        Returns:
            List of KPI metrics with sparkline-compatible trend data.
        """
        logger.info("Fetching KPI metrics from core service")

        # Generate sparkline points as numeric SVG polyline coordinates
        # Format: "x1,y1 x2,y2 x3,y3..." where viewBox is "0 0 50 24"
        return [
            {
                "label": "Total NAV",
                "value": "$2.4B",
                "is_positive": True,
                "trend_data": "0,20 10,15 20,18 30,12 40,8 50,5",
            },
            {
                "label": "Daily P&L",
                "value": "+$12.5M",
                "is_positive": True,
                "trend_data": "0,18 10,16 20,14 30,10 40,12 50,8",
            },
            {
                "label": "YTD Return",
                "value": "+18.2%",
                "is_positive": True,
                "trend_data": "0,22 10,18 20,16 30,14 40,10 50,6",
            },
            {
                "label": "Net Exposure",
                "value": "72%",
                "is_positive": True,
                "trend_data": "0,12 10,14 20,10 30,12 40,11 50,10",
            },
        ]

    async def get_portfolio_holdings(self) -> list[dict]:
        """
        Get portfolio holdings for summary cards.

        Returns:
            List of portfolio holdings
        """
        logger.info("Fetching portfolio holdings from core service")

        # Mock portfolio holdings data
        return [
            {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "shares": 150.0,
                "avg_cost": 175.0,
                "current_price": 189.5,
                "daily_change_pct": 1.25,
                "asset_class": "Technology",
            },
            {
                "symbol": "MSFT",
                "name": "Microsoft Corp.",
                "shares": 100.0,
                "avg_cost": 350.0,
                "current_price": 402.1,
                "daily_change_pct": 0.85,
                "asset_class": "Technology",
            },
            {
                "symbol": "JPM",
                "name": "JPMorgan Chase",
                "shares": 200.0,
                "avg_cost": 140.0,
                "current_price": 175.3,
                "daily_change_pct": -0.45,
                "asset_class": "Finance",
            },
        ]
