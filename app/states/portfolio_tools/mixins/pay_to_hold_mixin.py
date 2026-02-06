"""
Pay To Hold Mixin - Tab-specific state for Pay To Hold data.

Provides auto-refresh background task and force refresh functionality.
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.services import PortfolioToolsService
from app.states.portfolio_tools.types import PayToHoldItem


class PayToHoldMixin(rx.State, mixin=True):
    """
    Mixin providing Pay To Hold data state with auto-refresh.
    """

    # Pay To Hold data
    pay_to_hold: list[PayToHoldItem] = []
    is_loading_pay_to_hold: bool = False
    pay_to_hold_last_updated: str = "—"
    pay_to_hold_auto_refresh: bool = True

    async def load_pay_to_hold_data(self):
        """Load Pay To Hold data from PortfolioToolsService."""
        self.is_loading_pay_to_hold = True
        try:
            service = PortfolioToolsService()
            self.pay_to_hold = await service.get_pay_to_hold()
            self.pay_to_hold_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            import logging

            logging.exception(f"Error loading pay to hold data: {e}")
        finally:
            self.is_loading_pay_to_hold = False

    @rx.event(background=True)
    async def start_pay_to_hold_auto_refresh(self):
        """Background task for Pay To Hold auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.pay_to_hold_auto_refresh:
                    break
                self.simulate_pay_to_hold_update()
            await asyncio.sleep(2)

    def toggle_pay_to_hold_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.pay_to_hold_auto_refresh = value
        if value:
            return type(self).start_pay_to_hold_auto_refresh

    def simulate_pay_to_hold_update(self):
        """Simulated delta update for demo - random PTH amount changes."""
        if not self.pay_to_hold_auto_refresh or len(self.pay_to_hold) < 1:
            return

        import random

        new_list = list(self.pay_to_hold)

        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            new_row = dict(old_row)

            # Simulate pth_amount changes
            if "pth_amount" in new_row and new_row["pth_amount"]:
                try:
                    val = float(str(new_row["pth_amount"]).replace(",", ""))
                    new_val = round(val * random.uniform(0.98, 1.02), 2)
                    new_row["pth_amount"] = f"{new_val:,.2f}"
                except (ValueError, TypeError):
                    pass

            new_list[idx] = new_row

        self.pay_to_hold = new_list
        self.pay_to_hold_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_pay_to_hold(self):
        """Force refresh pay to hold data with loading overlay."""
        if self.is_loading_pay_to_hold:
            return
        self.is_loading_pay_to_hold = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = PortfolioToolsService()
            self.pay_to_hold = await service.get_pay_to_hold()
            self.pay_to_hold_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        finally:
            self.is_loading_pay_to_hold = False
