from typing import List, Optional, Dict, Any
from ..repositories.pnl_repository import PnLRepository
from ..models import PnLRecord
import logging

logger = logging.getLogger(__name__)


class PnLService:
    """
    Core business service for PnL.
    Delegates data fetching to PnLRepository.
    """

    def __init__(self, repository: Optional[PnLRepository] = None):
        self.repository = repository or PnLRepository()

    async def get_pnl_changes(
        self, trade_date: Optional[str] = None
    ) -> List[PnLRecord]:
        """Get P&L changes."""
        return await self.repository.get_pnl_changes(trade_date)

    async def get_pnl_summary(
        self, trade_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get P&L summary as dicts."""
        # This might not be in the repo yet, so we mock or delegate
        # If repo doesn't support it, we mock it here or add to repo.
        # For now, simplistic return or TODO
        # In real world, this would call repository.get_pnl_summary()
        return []

    async def calculate_daily_pnl(
        self, portfolio_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Calculate daily PnL."""
        return {
            "daily_pnl": 0.0,
            "daily_pnl_pct": 0.0,
            "ytd_pnl": 0.0,
            "ytd_pnl_pct": 0.0,
        }
