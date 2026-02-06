"""
Stock Screener Mixin - Tab-specific state for Stock Screener data.

Provides auto-refresh background task and force refresh functionality.
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.services import DatabaseService
from app.states.instruments.types import StockScreenerItem


class StockScreenerMixin(rx.State, mixin=True):
    """
    Mixin providing Stock Screener data state with auto-refresh.
    """

    # Stock Screener data
    stock_screener: list[StockScreenerItem] = []
    is_loading_stock_screener: bool = False
    stock_screener_last_updated: str = "—"
    stock_screener_auto_refresh: bool = True

    async def load_stock_screener_data(self):
        """Load Stock Screener data from DatabaseService."""
        self.is_loading_stock_screener = True
        try:
            service = DatabaseService()
            self.stock_screener = await service.get_stock_screener()
            self.stock_screener_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error loading stock screener data: {e}")
        finally:
            self.is_loading_stock_screener = False

    @rx.event(background=True)
    async def start_stock_screener_auto_refresh(self):
        """Background task for Stock Screener auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.stock_screener_auto_refresh:
                    break
                self.simulate_stock_screener_update()
            await asyncio.sleep(2)

    def toggle_stock_screener_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.stock_screener_auto_refresh = value
        if value:
            return type(self).start_stock_screener_auto_refresh

    def simulate_stock_screener_update(self):
        """Simulated delta update for demo - random price/cap changes."""
        if not self.stock_screener_auto_refresh or len(self.stock_screener) < 1:
            return

        import random

        new_list = list(self.stock_screener)

        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            new_row = dict(old_row)

            # Simulate last_price changes
            if "last_price" in new_row and new_row["last_price"]:
                try:
                    val = float(str(new_row["last_price"]).replace(",", ""))
                    new_val = round(val * random.uniform(0.995, 1.005), 2)
                    new_row["last_price"] = f"{new_val:,.2f}"
                except (ValueError, TypeError):
                    pass

            # Simulate mkt_cap_usd changes
            if "mkt_cap_usd" in new_row and new_row["mkt_cap_usd"]:
                try:
                    val = float(str(new_row["mkt_cap_usd"]).replace(",", ""))
                    new_val = round(val * random.uniform(0.99, 1.01), 2)
                    new_row["mkt_cap_usd"] = f"{new_val:,.2f}"
                except (ValueError, TypeError):
                    pass

            new_list[idx] = new_row

        self.stock_screener = new_list
        self.stock_screener_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_stock_screener(self):
        """Force refresh stock screener data with loading overlay."""
        if self.is_loading_stock_screener:
            return
        self.is_loading_stock_screener = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = DatabaseService()
            self.stock_screener = await service.get_stock_screener()
            self.stock_screener_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing stock screener: {e}")
        finally:
            self.is_loading_stock_screener = False
