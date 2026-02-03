"""
P&L (Profit & Loss) Service for Portfolio Management Tool.

Delegates to pmt_core.services.PnLService.
"""

import logging
from typing import Optional

from pmt_core.services import PnLService as CorePnLService
from pmt_core import PnLRecord

logger = logging.getLogger(__name__)


class PnLService:
    """
    Service for P&L calculation and data retrieval.
    """

    def __init__(self):
        """Initialize P&L service."""
        self.core_service = CorePnLService()

    async def get_pnl_summary(self, trade_date: Optional[str] = None) -> list[dict]:
        """Get P&L summary."""
        return await self.core_service.get_pnl_summary(trade_date)

    async def get_pnl_changes(
        self, trade_date: Optional[str] = None, period: str = "1d"
    ) -> list[PnLRecord]:
        """Get P&L changes."""
        return await self.core_service.get_pnl_changes(trade_date)

    async def get_pnl_by_currency(self, trade_date: Optional[str] = None) -> list[dict]:
        """Get P&L broken down by currency."""
        # TODO: Implement in Core Service
        logger.warning(
            "get_pnl_by_currency not implemented in core yet, returning empty."
        )
        return []

    async def calculate_daily_pnl(self, portfolio_id: Optional[str] = None) -> dict:
        """Calculate total daily P&L."""
        return await self.core_service.calculate_daily_pnl(portfolio_id)

    async def get_kpi_metrics(self) -> list[dict]:
        """Get KPI metrics."""
        # TODO: Implement in Core Service
        # For now return mock to avoid breaking UI if it expects data
        return [
            {
                "label": "Total NAV",
                "value": "$2.4B",
                "is_positive": True,
                "trend_data": "+2.5%",
            },
            {
                "label": "Daily P&L",
                "value": "+$12.5M",
                "is_positive": True,
                "trend_data": "+0.5%",
            },
        ]

    async def get_currency_pnl(self) -> list[dict]:
        """Alias for get_pnl_by_currency."""
        return await self.get_pnl_by_currency()

    async def get_pnl_full(self, trade_date: Optional[str] = None) -> list[PnLRecord]:
        """Get full P&L detailed view."""
        # TODO: Implement in Core Service. Mock data for testing.
        return [
            {
                "id": 1,
                "trade_date": "2026-01-31",
                "underlying": "Toyota Motor",
                "ticker": "7203.T",
                "pnl_ytd": "$1,234,567",
                "pnl_chg_1d": "$12,345",
                "pnl_chg_1w": "$45,678",
                "pnl_chg_1m": "$123,456",
                "pnl_chg_pct_1d": "+1.2%",
                "pnl_chg_pct_1w": "+3.5%",
                "pnl_chg_pct_1m": "+8.7%",
            },
            {
                "id": 2,
                "trade_date": "2026-01-31",
                "underlying": "Sony Group",
                "ticker": "6758.T",
                "pnl_ytd": "$987,654",
                "pnl_chg_1d": "-$8,765",
                "pnl_chg_1w": "$23,456",
                "pnl_chg_1m": "$67,890",
                "pnl_chg_pct_1d": "-0.9%",
                "pnl_chg_pct_1w": "+2.1%",
                "pnl_chg_pct_1m": "+5.4%",
            },
            {
                "id": 3,
                "trade_date": "2026-01-31",
                "underlying": "Nintendo",
                "ticker": "7974.T",
                "pnl_ytd": "$2,345,678",
                "pnl_chg_1d": "$34,567",
                "pnl_chg_1w": "$78,901",
                "pnl_chg_1m": "$234,567",
                "pnl_chg_pct_1d": "+2.3%",
                "pnl_chg_pct_1w": "+4.8%",
                "pnl_chg_pct_1m": "+12.1%",
            },
            {
                "id": 4,
                "trade_date": "2026-01-31",
                "underlying": "SoftBank Group",
                "ticker": "9984.T",
                "pnl_ytd": "($456,789)",
                "pnl_chg_1d": "-$45,678",
                "pnl_chg_1w": "-$89,012",
                "pnl_chg_1m": "($156,789)",
                "pnl_chg_pct_1d": "-3.2%",
                "pnl_chg_pct_1w": "-5.6%",
                "pnl_chg_pct_1m": "-9.8%",
            },
            {
                "id": 5,
                "trade_date": "2026-01-31",
                "underlying": "Keyence",
                "ticker": "6861.T",
                "pnl_ytd": "$3,456,789",
                "pnl_chg_1d": "$56,789",
                "pnl_chg_1w": "$123,456",
                "pnl_chg_1m": "$345,678",
                "pnl_chg_pct_1d": "+1.8%",
                "pnl_chg_pct_1w": "+5.2%",
                "pnl_chg_pct_1m": "+15.3%",
            },
            {
                "id": 6,
                "trade_date": "2026-01-31",
                "underlying": "Fast Retailing",
                "ticker": "9983.T",
                "pnl_ytd": "$567,890",
                "pnl_chg_1d": "$6,789",
                "pnl_chg_1w": "$12,345",
                "pnl_chg_1m": "$56,789",
                "pnl_chg_pct_1d": "+0.7%",
                "pnl_chg_pct_1w": "+1.9%",
                "pnl_chg_pct_1m": "+4.2%",
            },
            {
                "id": 7,
                "trade_date": "2026-01-31",
                "underlying": "Tokyo Electron",
                "ticker": "8035.T",
                "pnl_ytd": "$1,890,123",
                "pnl_chg_1d": "-$23,456",
                "pnl_chg_1w": "$45,678",
                "pnl_chg_1m": "$189,012",
                "pnl_chg_pct_1d": "-1.1%",
                "pnl_chg_pct_1w": "+2.8%",
                "pnl_chg_pct_1m": "+7.6%",
            },
            {
                "id": 8,
                "trade_date": "2026-01-31",
                "underlying": "Shin-Etsu Chemical",
                "ticker": "4063.T",
                "pnl_ytd": "$789,012",
                "pnl_chg_1d": "$7,890",
                "pnl_chg_1w": "$15,678",
                "pnl_chg_1m": "$78,901",
                "pnl_chg_pct_1d": "+0.9%",
                "pnl_chg_pct_1w": "+2.3%",
                "pnl_chg_pct_1m": "+6.1%",
            },
            {
                "id": 9,
                "trade_date": "2026-01-31",
                "underlying": "Hitachi",
                "ticker": "6501.T",
                "pnl_ytd": "$1,234,567",
                "pnl_chg_1d": "$23,456",
                "pnl_chg_1w": "$56,789",
                "pnl_chg_1m": "$123,456",
                "pnl_chg_pct_1d": "+1.5%",
                "pnl_chg_pct_1w": "+3.9%",
                "pnl_chg_pct_1m": "+9.2%",
            },
            {
                "id": 10,
                "trade_date": "2026-01-31",
                "underlying": "Mitsubishi UFJ",
                "ticker": "8306.T",
                "pnl_ytd": "($234,567)",
                "pnl_chg_1d": "-$12,345",
                "pnl_chg_1w": "-$34,567",
                "pnl_chg_1m": "($78,901)",
                "pnl_chg_pct_1d": "-1.8%",
                "pnl_chg_pct_1w": "-4.2%",
                "pnl_chg_pct_1m": "-7.5%",
            },
            {
                "id": 11,
                "trade_date": "2026-01-31",
                "underlying": "Recruit Holdings",
                "ticker": "6098.T",
                "pnl_ytd": "$890,123",
                "pnl_chg_1d": "$8,901",
                "pnl_chg_1w": "$17,890",
                "pnl_chg_1m": "$89,012",
                "pnl_chg_pct_1d": "+1.0%",
                "pnl_chg_pct_1w": "+2.5%",
                "pnl_chg_pct_1m": "+6.8%",
            },
            {
                "id": 12,
                "trade_date": "2026-01-31",
                "underlying": "Daikin Industries",
                "ticker": "6367.T",
                "pnl_ytd": "$456,789",
                "pnl_chg_1d": "$4,567",
                "pnl_chg_1w": "$9,012",
                "pnl_chg_1m": "$45,678",
                "pnl_chg_pct_1d": "+0.6%",
                "pnl_chg_pct_1w": "+1.7%",
                "pnl_chg_pct_1m": "+3.9%",
            },
            {
                "id": 13,
                "trade_date": "2026-01-31",
                "underlying": "KDDI",
                "ticker": "9433.T",
                "pnl_ytd": "$345,678",
                "pnl_chg_1d": "-$3,456",
                "pnl_chg_1w": "$6,789",
                "pnl_chg_1m": "$34,567",
                "pnl_chg_pct_1d": "-0.5%",
                "pnl_chg_pct_1w": "+1.2%",
                "pnl_chg_pct_1m": "+3.2%",
            },
            {
                "id": 14,
                "trade_date": "2026-01-31",
                "underlying": "Fanuc",
                "ticker": "6954.T",
                "pnl_ytd": "$678,901",
                "pnl_chg_1d": "$6,789",
                "pnl_chg_1w": "$13,456",
                "pnl_chg_1m": "$67,890",
                "pnl_chg_pct_1d": "+0.8%",
                "pnl_chg_pct_1w": "+2.1%",
                "pnl_chg_pct_1m": "+5.5%",
            },
            {
                "id": 15,
                "trade_date": "2026-01-31",
                "underlying": "Murata Manufacturing",
                "ticker": "6981.T",
                "pnl_ytd": "$1,567,890",
                "pnl_chg_1d": "$15,678",
                "pnl_chg_1w": "$31,234",
                "pnl_chg_1m": "$156,789",
                "pnl_chg_pct_1d": "+1.3%",
                "pnl_chg_pct_1w": "+3.1%",
                "pnl_chg_pct_1m": "+8.1%",
            },
        ]
