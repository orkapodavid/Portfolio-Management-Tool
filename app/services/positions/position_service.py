"""
Position Service for Portfolio Management Tool.

This service handles position data fetching and processing.
Delegates to pmt_core.services.PositionService.
"""

import logging
from typing import Optional

from pmt_core.services import PositionService as CorePositionService
from pmt_core import PositionRecord

logger = logging.getLogger(__name__)


class PositionService:
    """
    Service for fetching and processing position data.
    """

    def __init__(self):
        """Initialize position service."""
        self.core_service = CorePositionService()

    async def get_positions(
        self, position_date: Optional[str] = None, account_id: Optional[str] = None
    ) -> list[PositionRecord]:
        """Get all positions for a given date."""
        return await self.core_service.get_positions(position_date)

    async def get_stock_positions(
        self, position_date: Optional[str] = None
    ) -> list[PositionRecord]:
        """Get stock positions only."""
        return await self.core_service.get_stock_positions(position_date)

    async def get_warrant_positions(
        self, position_date: Optional[str] = None
    ) -> list[PositionRecord]:
        """Get warrant positions only."""
        return await self.core_service.get_warrant_positions(position_date)

    async def get_bond_positions(
        self, position_date: Optional[str] = None
    ) -> list[PositionRecord]:
        """Get bond positions only."""
        return await self.core_service.get_bond_positions(position_date)

    async def get_trade_summary(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> list[PositionRecord]:
        """Get trade summary for date range."""
        # Mock data for trade summary
        return [
            {
                "id": i,
                "deal_num": f"TDEAL{i:03d}",
                "detail_id": f"TD{i:03d}",
                "ticker": f"TRD{i}",
                "underlying": f"TRD{i} US Equity",
                "account_id": f"ACC00{i % 3 + 1}",
                "company_name": f"Trade Co {i}",
                "sec_id": f"TSEC{i:06d}",
                "sec_type": ["Equity", "Warrant", "Bond"][i % 3],
                "subtype": ["Common", "Call", "Corporate"][i % 3],
                "currency": "USD",
                "closing_date": "2026-01-31",
                "divisor": f"{1.0 + i * 0.05:.4f}",
            }
            for i in range(8)
        ]
