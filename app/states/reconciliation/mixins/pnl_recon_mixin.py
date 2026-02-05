"""
PnL Recon Mixin - Force Refresh Pattern

Uses force refresh button instead of auto-refresh for static data.
"""

import reflex as rx
from app.services import DatabaseService
from app.states.reconciliation.types import PnLReconItem


class PnLReconMixin(rx.State, mixin=True):
    """
    Mixin providing PnL Recon data state with force refresh pattern.
    """

    pnl_recon: list[PnLReconItem] = []
    is_loading_pnl_recon: bool = False
    pnl_recon_error: str = ""

    # Status bar state (per-tab)
    pnl_recon_last_updated: str = "—"

    pnl_recon_search: str = ""

    async def load_pnl_recon_data(self):
        """Load PnL Recon data."""
        self.is_loading_pnl_recon = True
        self.pnl_recon_error = ""
        try:
            service = DatabaseService()
            self.pnl_recon = await service.get_pnl_recon()
        except Exception as e:
            self.pnl_recon_error = str(e)
            import logging

            logging.exception(f"Error loading PnL Recon: {e}")
        finally:
            self.is_loading_pnl_recon = False
            from datetime import datetime

            self.pnl_recon_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_pnl_recon(self):
        """Force refresh - reloads data from service (all cells flash).
        
        Uses yield + is_loading guard to:
        1. Prevent multiple clicks while loading
        2. Show loading overlay immediately
        """
        if self.is_loading_pnl_recon:
            return  # Debounce: ignore clicks while loading
        
        import asyncio
        self.is_loading_pnl_recon = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.5)  # Brief delay to show loading overlay
        await self.load_pnl_recon_data()

    def set_pnl_recon_search(self, query: str):
        self.pnl_recon_search = query

    @rx.var(cache=True)
    def filtered_pnl_recon(self) -> list[PnLReconItem]:
        data = self.pnl_recon
        if self.pnl_recon_search:
            query = self.pnl_recon_search.lower()
            data = [
                item
                for item in data
                if query in item.get("underlying", "").lower()
                or query in item.get("deal_num", "").lower()
            ]
        return data
