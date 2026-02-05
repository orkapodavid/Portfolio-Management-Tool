"""
Settlement Recon Mixin - Force Refresh Pattern

Uses force refresh button instead of auto-refresh for static data.
"""

import reflex as rx
from app.services import DatabaseService
from app.states.reconciliation.types import SettlementReconItem


class SettlementReconMixin(rx.State, mixin=True):
    """
    Mixin providing Settlement Recon data state with force refresh pattern.
    """

    settlement_recon: list[SettlementReconItem] = []
    is_loading_settlement_recon: bool = False
    settlement_recon_error: str = ""

    # Status bar state (per-tab)
    settlement_recon_last_updated: str = "—"

    settlement_recon_search: str = ""

    async def load_settlement_recon_data(self):
        """Load Settlement recon data."""
        self.is_loading_settlement_recon = True
        self.settlement_recon_error = ""
        try:
            service = DatabaseService()
            self.settlement_recon = await service.get_settlement_recon()
        except Exception as e:
            self.settlement_recon_error = str(e)
            import logging

            logging.exception(f"Error loading Settlement recon: {e}")
        finally:
            self.is_loading_settlement_recon = False
            from datetime import datetime

            self.settlement_recon_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

    async def force_refresh_settlement_recon(self):
        """Force refresh - reloads data from service (all cells flash).
        
        Uses yield + is_loading guard to:
        1. Prevent multiple clicks while loading
        2. Show loading overlay immediately
        """
        if self.is_loading_settlement_recon:
            return  # Debounce: ignore clicks while loading
        
        import asyncio
        self.is_loading_settlement_recon = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.5)  # Brief delay to show loading overlay
        await self.load_settlement_recon_data()

    def set_settlement_recon_search(self, query: str):
        self.settlement_recon_search = query

    @rx.var(cache=True)
    def filtered_settlement_recon(self) -> list[SettlementReconItem]:
        data = self.settlement_recon
        if self.settlement_recon_search:
            query = self.settlement_recon_search.lower()
            data = [
                item
                for item in data
                if query in item.get("ticker", "").lower()
                or query in item.get("company_name", "").lower()
            ]
        return data
