"""
CB Installments Mixin - Tab-specific state for CB Installments data.

Provides auto-refresh background task and force refresh functionality.
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.states.portfolio_tools.types import CBInstallmentItem
import logging
import random
from app.services import services

class CBInstallmentsMixin(rx.State, mixin=True):
    """
    Mixin providing CB Installments data state with auto-refresh.
    """

    # CB Installments data
    cb_installments: list[CBInstallmentItem] = []
    is_loading_cb_installments: bool = False
    cb_installments_last_updated: str = "—"
    cb_installments_auto_refresh: bool = True
    cb_installments_position_date: str = datetime.now().strftime("%Y-%m-%d")

    async def set_cb_installments_position_date(self, value: str):
        """Set position date and reload data."""
        self.cb_installments_position_date = value
        yield
        await self.load_cb_installments_data()

    async def load_cb_installments_data(self):
        """Load CB Installments data from PortfolioToolsService."""
        self.is_loading_cb_installments = True
        try:
            self.cb_installments = await services.portfolio_tools.get_cb_installments(self.cb_installments_position_date)
            self.cb_installments_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error loading CB installments data: {e}")
        finally:
            self.is_loading_cb_installments = False

    @rx.event(background=True)
    async def start_cb_installments_auto_refresh(self):
        """Background task for CB Installments auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.cb_installments_auto_refresh:
                    break
                self.simulate_cb_installments_update()
            await asyncio.sleep(2)

    def toggle_cb_installments_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.cb_installments_auto_refresh = value
        if value:
            return type(self).start_cb_installments_auto_refresh

    def simulate_cb_installments_update(self):
        """Simulated delta update for demo - random amount changes."""
        if not self.cb_installments_auto_refresh or len(self.cb_installments) < 1:
            return

        new_list = list(self.cb_installments)

        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            new_row = dict(old_row)

            # Simulate installment_amount changes
            if "installment_amount" in new_row and new_row["installment_amount"]:
                try:
                    val = float(str(new_row["installment_amount"]).replace(",", ""))
                    new_val = round(val * random.uniform(0.98, 1.02), 2)
                    new_row["installment_amount"] = f"{new_val:,.2f}"
                except (ValueError, TypeError):
                    pass

            new_list[idx] = new_row

        self.cb_installments = new_list
        self.cb_installments_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_cb_installments(self):
        """Force refresh CB installments data with loading overlay."""
        if self.is_loading_cb_installments:
            return
        self.is_loading_cb_installments = True
        yield
        await asyncio.sleep(0.3)
        try:
            self.cb_installments = await services.portfolio_tools.get_cb_installments(self.cb_installments_position_date)
            self.cb_installments_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        finally:
            self.is_loading_cb_installments = False
