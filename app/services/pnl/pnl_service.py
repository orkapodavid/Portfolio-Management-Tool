"""
P&L (Profit & Loss) Service for Portfolio Management Tool.

Delegates to pmt_core.services.PnLService.
"""

import logging
from typing import Optional

from pmt_core.services import PnLService as CorePnLService
from pmt_core import PnLRecord

from app.ag_grid_constants import GridId
from app.services.notifications.notification_registry import NotificationRegistry
from app.services.notifications.notification_constants import (
    NotificationCategory,
    NotificationIcon,
    NotificationColor,
)

logger = logging.getLogger(__name__)


# === NOTIFICATION PROVIDERS ===
def _get_pnl_notifications() -> list[dict]:
    """Mock PnL notifications for P&L threshold alerts."""
    return [
        {
            "id": "pnl-001",
            "category": NotificationCategory.ALERTS,
            "title": "PnL Alert",
            "message": "AAPL daily PnL exceeded threshold",
            "time_ago": "10 mins ago",
            "is_read": False,
            "icon": NotificationIcon.DOLLAR_SIGN,
            "color": NotificationColor.YELLOW,
            "module": "PnL",
            "subtab": "PnL Change",
            "row_id": "AAPL",
            "grid_id": GridId.PNL_CHANGE,
            "ticker": "AAPL",
        },
    ]


# Register provider at module load
NotificationRegistry.register("pnl", _get_pnl_notifications)


class PnLService:
    """
    Service for P&L calculation and data retrieval.
    Delegates to pmt_core PnLService for data.
    """

    def __init__(self):
        """Initialize P&L service."""
        self.core_service = CorePnLService()

    async def get_pnl_summary(self, trade_date: Optional[str] = None) -> list[dict]:
        """Get P&L summary. Delegates to core."""
        return await self.core_service.get_pnl_summary(trade_date)

    async def get_pnl_changes(
        self, trade_date: Optional[str] = None, period: str = "1d"
    ) -> list[PnLRecord]:
        """Get P&L changes. Delegates to core."""
        return await self.core_service.get_pnl_changes(trade_date)

    async def get_pnl_by_currency(self, trade_date: Optional[str] = None) -> list[dict]:
        """Get P&L by currency. Delegates to core."""
        return await self.core_service.get_pnl_by_currency(trade_date)

    async def calculate_daily_pnl(self, portfolio_id: Optional[str] = None) -> dict:
        """Calculate total daily P&L. Delegates to core."""
        return await self.core_service.calculate_daily_pnl(portfolio_id)

    async def get_kpi_metrics(self) -> list[dict]:
        """Get KPI metrics. Delegates to core."""
        return await self.core_service.get_kpi_metrics()

    async def get_currency_pnl(self) -> list[dict]:
        """Alias for get_pnl_by_currency. Delegates to core."""
        return await self.core_service.get_pnl_by_currency()

    async def get_pnl_full(self, trade_date: Optional[str] = None) -> list[PnLRecord]:
        """Get full P&L detailed view. Delegates to core."""
        return await self.core_service.get_pnl_full(trade_date)
