"""
PPS Recon Mixin - Force Refresh Pattern

Uses force refresh button instead of auto-refresh for static data.
"""

import reflex as rx
from app.states.reconciliation.types import PPSReconItem
import logging
from app.services import services

class PPSReconMixin(rx.State, mixin=True):
    """
    Mixin providing PPS Recon data state with force refresh pattern.
    """

    pps_recon: list[PPSReconItem] = []
    is_loading_pps_recon: bool = False
    pps_recon_error: str = ""

    # Status bar state (per-tab)
    pps_recon_last_updated: str = "—"

    pps_recon_search: str = ""
    pps_recon_position_date: str = ""

    async def set_pps_recon_position_date(self, value: str):
        """Set position date and reload data."""
        self.pps_recon_position_date = value
        yield
        await self.load_pps_recon_data()

    async def load_pps_recon_data(self):
        """Load PPS recon data."""
        self.is_loading_pps_recon = True
        self.pps_recon_error = ""
        try:
            self.pps_recon = await services.reconciliation.get_pps_recon(self.pps_recon_position_date)
        except Exception as e:
            self.pps_recon_error = str(e)

            logging.exception(f"Error loading PPS recon: {e}")
        finally:
            self.is_loading_pps_recon = False
            from datetime import datetime

            self.pps_recon_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_pps_recon(self):
        """Force refresh - reloads data from service (all cells flash).
        
        Uses yield + is_loading guard to:
        1. Prevent multiple clicks while loading
        2. Show loading overlay immediately
        """
        if self.is_loading_pps_recon:
            return  # Debounce: ignore clicks while loading
        
        import asyncio
        self.is_loading_pps_recon = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.5)  # Brief delay to show loading overlay
        await self.load_pps_recon_data()

    def set_pps_recon_search(self, query: str):
        self.pps_recon_search = query

    @rx.var(cache=True)
    def filtered_pps_recon(self) -> list[PPSReconItem]:
        data = self.pps_recon
        if self.pps_recon_search:
            query = self.pps_recon_search.lower()
            data = [
                item
                for item in data
                if query in item.get("ticker", "").lower()
                or query in item.get("company_name", "").lower()
            ]
        return data
