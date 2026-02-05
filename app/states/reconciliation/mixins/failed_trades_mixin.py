"""
Failed Trades Mixin - Force Refresh Pattern

Uses force refresh button instead of auto-refresh for static data.
"""

import reflex as rx
from app.services import DatabaseService
from app.states.reconciliation.types import FailedTradeItem


class FailedTradesMixin(rx.State, mixin=True):
    """
    Mixin providing Failed Trades data state with force refresh pattern.
    """

    failed_trades: list[FailedTradeItem] = []
    is_loading_failed_trades: bool = False
    failed_trades_error: str = ""

    # Status bar state (per-tab)
    failed_trades_last_updated: str = "—"

    failed_trades_search: str = ""

    async def load_failed_trades_data(self):
        """Load Failed Trades data."""
        self.is_loading_failed_trades = True
        self.failed_trades_error = ""
        try:
            service = DatabaseService()
            self.failed_trades = await service.get_failed_trades()
        except Exception as e:
            self.failed_trades_error = str(e)
            import logging

            logging.exception(f"Error loading Failed Trades: {e}")
        finally:
            self.is_loading_failed_trades = False
            from datetime import datetime

            self.failed_trades_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

    async def force_refresh_failed_trades(self):
        """Force refresh - reloads data from service (all cells flash).
        
        Uses yield + is_loading guard to:
        1. Prevent multiple clicks while loading
        2. Show loading overlay immediately
        """
        if self.is_loading_failed_trades:
            return  # Debounce: ignore clicks while loading
        
        import asyncio
        self.is_loading_failed_trades = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.5)  # Brief delay to show loading overlay
        await self.load_failed_trades_data()

    def set_failed_trades_search(self, query: str):
        self.failed_trades_search = query

    @rx.var(cache=True)
    def filtered_failed_trades(self) -> list[FailedTradeItem]:
        data = self.failed_trades
        if self.failed_trades_search:
            query = self.failed_trades_search.lower()
            data = [
                item
                for item in data
                if query in item.get("ticker", "").lower()
                or query in item.get("company_name", "").lower()
            ]
        return data
