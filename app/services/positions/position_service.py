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
        # TODO: Implement in Core Service
        logger.warning(
            "get_trade_summary not implemented in core yet, returning empty."
        )
        return []
