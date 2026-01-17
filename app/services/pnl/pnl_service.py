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
        # TODO: Implement in Core Service
        return []
