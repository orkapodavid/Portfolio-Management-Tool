"""
Stock Borrow Mixin - Tab-specific state for Stock Borrow data.

Provides auto-refresh background task and force refresh functionality.
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.services import PortfolioToolsService
from app.states.portfolio_tools.types import StockBorrowItem
import logging
import random

class StockBorrowMixin(rx.State, mixin=True):
    """
    Mixin providing Stock Borrow data state with auto-refresh.
    """

    # Stock Borrow data
    stock_borrow: list[StockBorrowItem] = []
    is_loading_stock_borrow: bool = False
    stock_borrow_last_updated: str = "—"
    stock_borrow_auto_refresh: bool = True

    async def load_stock_borrow_data(self):
        """Load Stock Borrow data from PortfolioToolsService."""
        self.is_loading_stock_borrow = True
        try:
            service = PortfolioToolsService()
            self.stock_borrow = await service.get_stock_borrow()
            self.stock_borrow_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error loading stock borrow data: {e}")
        finally:
            self.is_loading_stock_borrow = False

    @rx.event(background=True)
    async def start_stock_borrow_auto_refresh(self):
        """Background task for Stock Borrow auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.stock_borrow_auto_refresh:
                    break
                self.simulate_stock_borrow_update()
            await asyncio.sleep(2)

    def toggle_stock_borrow_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.stock_borrow_auto_refresh = value
        if value:
            return type(self).start_stock_borrow_auto_refresh

    def simulate_stock_borrow_update(self):
        """Simulated delta update for demo - random borrow rate changes."""
        if not self.stock_borrow_auto_refresh or len(self.stock_borrow) < 1:
            return

        new_list = list(self.stock_borrow)

        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            new_row = dict(old_row)

            # Simulate borrow_rate changes
            if "borrow_rate" in new_row and new_row["borrow_rate"]:
                try:
                    val_str = str(new_row["borrow_rate"]).replace("%", "")
                    val = float(val_str)
                    new_val = round(val * random.uniform(0.95, 1.05), 2)
                    new_row["borrow_rate"] = f"{new_val:.2f}%"
                except (ValueError, TypeError):
                    pass

            new_list[idx] = new_row

        self.stock_borrow = new_list
        self.stock_borrow_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_stock_borrow(self):
        """Force refresh stock borrow data with loading overlay."""
        if self.is_loading_stock_borrow:
            return
        self.is_loading_stock_borrow = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = PortfolioToolsService()
            self.stock_borrow = await service.get_stock_borrow()
            self.stock_borrow_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        finally:
            self.is_loading_stock_borrow = False
