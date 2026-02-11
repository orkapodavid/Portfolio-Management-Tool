"""
Excess Amount Mixin - Tab-specific state for Excess Amount data.

Provides auto-refresh background task and force refresh functionality.
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.services import PortfolioToolsService
from app.states.portfolio_tools.types import ExcessAmountItem


class ExcessAmountMixin(rx.State, mixin=True):
    """
    Mixin providing Excess Amount data state with auto-refresh.
    """

    # Excess Amount data
    excess_amount: list[ExcessAmountItem] = []
    is_loading_excess_amount: bool = False
    excess_amount_last_updated: str = "—"
    excess_amount_auto_refresh: bool = True
    excess_amount_position_date: str = datetime.now().strftime("%Y-%m-%d")

    async def set_excess_amount_position_date(self, value: str):
        """Set position date and reload data."""
        self.excess_amount_position_date = value
        yield
        await self.load_excess_amount_data()

    async def load_excess_amount_data(self):
        """Load Excess Amount data from PortfolioToolsService."""
        self.is_loading_excess_amount = True
        try:
            service = PortfolioToolsService()
            self.excess_amount = await service.get_excess_amount(self.excess_amount_position_date)
            self.excess_amount_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error loading excess amount data: {e}")
        finally:
            self.is_loading_excess_amount = False

    @rx.event(background=True)
    async def start_excess_amount_auto_refresh(self):
        """Background task for Excess Amount auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.excess_amount_auto_refresh:
                    break
                self.simulate_excess_amount_update()
            await asyncio.sleep(2)

    def toggle_excess_amount_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.excess_amount_auto_refresh = value
        if value:
            return type(self).start_excess_amount_auto_refresh

    def simulate_excess_amount_update(self):
        """Simulated delta update for demo - random excess amount changes."""
        if not self.excess_amount_auto_refresh or len(self.excess_amount) < 1:
            return

        import random

        new_list = list(self.excess_amount)

        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            new_row = dict(old_row)

            # Simulate excess_amount field changes
            if "excess_amount" in new_row and new_row["excess_amount"]:
                try:
                    val = float(str(new_row["excess_amount"]).replace(",", ""))
                    new_val = round(val * random.uniform(0.95, 1.05), 2)
                    new_row["excess_amount"] = f"{new_val:,.2f}"
                except (ValueError, TypeError):
                    pass

            new_list[idx] = new_row

        self.excess_amount = new_list
        self.excess_amount_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_excess_amount(self):
        """Force refresh excess amount data with loading overlay."""
        if self.is_loading_excess_amount:
            return
        self.is_loading_excess_amount = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = PortfolioToolsService()
            self.excess_amount = await service.get_excess_amount(self.excess_amount_position_date)
            self.excess_amount_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        finally:
            self.is_loading_excess_amount = False
