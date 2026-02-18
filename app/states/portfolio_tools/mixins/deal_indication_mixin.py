"""
Deal Indication Mixin - Tab-specific state for Deal Indication data.

Provides auto-refresh background task and force refresh functionality.
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.services import PortfolioToolsService
from app.states.portfolio_tools.types import DealIndicationItem
import logging
import random

class DealIndicationMixin(rx.State, mixin=True):
    """
    Mixin providing Deal Indication data state with auto-refresh.
    """

    # Deal Indication data
    deal_indication: list[DealIndicationItem] = []
    is_loading_deal_indication: bool = False
    deal_indication_last_updated: str = "—"
    deal_indication_auto_refresh: bool = True

    async def load_deal_indication_data(self):
        """Load Deal Indication data from PortfolioToolsService."""
        self.is_loading_deal_indication = True
        try:
            service = PortfolioToolsService()
            self.deal_indication = await service.get_deal_indication()
            self.deal_indication_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error loading deal indication data: {e}")
        finally:
            self.is_loading_deal_indication = False

    @rx.event(background=True)
    async def start_deal_indication_auto_refresh(self):
        """Background task for Deal Indication auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.deal_indication_auto_refresh:
                    break
                self.simulate_deal_indication_update()
            await asyncio.sleep(2)

    def toggle_deal_indication_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.deal_indication_auto_refresh = value
        if value:
            return type(self).start_deal_indication_auto_refresh

    def simulate_deal_indication_update(self):
        """Simulated delta update for demo - random amount changes."""
        if not self.deal_indication_auto_refresh or len(self.deal_indication) < 1:
            return

        new_list = list(self.deal_indication)

        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            new_row = dict(old_row)

            # Simulate indication_amount changes
            if "indication_amount" in new_row and new_row["indication_amount"]:
                try:
                    val = float(str(new_row["indication_amount"]).replace(",", ""))
                    new_val = round(val * random.uniform(0.98, 1.02), 2)
                    new_row["indication_amount"] = f"{new_val:,.2f}"
                except (ValueError, TypeError):
                    pass

            new_list[idx] = new_row

        self.deal_indication = new_list
        self.deal_indication_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_deal_indication(self):
        """Force refresh deal indication data with loading overlay."""
        if self.is_loading_deal_indication:
            return
        self.is_loading_deal_indication = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = PortfolioToolsService()
            self.deal_indication = await service.get_deal_indication()
            self.deal_indication_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        finally:
            self.is_loading_deal_indication = False
