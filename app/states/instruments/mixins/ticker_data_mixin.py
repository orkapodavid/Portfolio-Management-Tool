"""
Ticker Data Mixin - Tab-specific state for Ticker Data.

Provides auto-refresh background task and force refresh functionality.
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.services import DatabaseService
from app.states.instruments.types import TickerDataItem


class TickerDataMixin(rx.State, mixin=True):
    """
    Mixin providing Ticker Data state with auto-refresh.
    """

    # Ticker Data
    ticker_data: list[TickerDataItem] = []
    is_loading_ticker_data: bool = False
    ticker_data_last_updated: str = "—"
    ticker_data_auto_refresh: bool = True

    async def load_ticker_data(self):
        """Load Ticker Data from DatabaseService."""
        self.is_loading_ticker_data = True
        try:
            service = DatabaseService()
            self.ticker_data = await service.get_ticker_data()
            self.ticker_data_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            import logging

            logging.exception(f"Error loading ticker data: {e}")
        finally:
            self.is_loading_ticker_data = False

    @rx.event(background=True)
    async def start_ticker_data_auto_refresh(self):
        """Background task for Ticker Data auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.ticker_data_auto_refresh:
                    break
                self.simulate_ticker_data_update()
            await asyncio.sleep(2)

    def toggle_ticker_data_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.ticker_data_auto_refresh = value
        if value:
            return type(self).start_ticker_data_auto_refresh

    def simulate_ticker_data_update(self):
        """Simulated delta update for demo - random price changes."""
        if not self.ticker_data_auto_refresh or len(self.ticker_data) < 1:
            return

        import random

        new_list = list(self.ticker_data)

        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            new_row = dict(old_row)

            # Simulate chg_1d_pct changes
            if "chg_1d_pct" in new_row and new_row["chg_1d_pct"]:
                try:
                    val_str = str(new_row["chg_1d_pct"]).replace("%", "").replace("+", "")
                    val = float(val_str)
                    new_val = round(val * random.uniform(0.9, 1.1), 2)
                    new_row["chg_1d_pct"] = f"{new_val:+.2f}%"
                except (ValueError, TypeError):
                    pass

            # Simulate fx_rate changes
            if "fx_rate" in new_row and new_row["fx_rate"]:
                try:
                    val = float(str(new_row["fx_rate"]).replace(",", ""))
                    new_val = round(val * random.uniform(0.9999, 1.0001), 4)
                    new_row["fx_rate"] = f"{new_val:.4f}"
                except (ValueError, TypeError):
                    pass

            new_list[idx] = new_row

        self.ticker_data = new_list
        self.ticker_data_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_ticker_data(self):
        """Force refresh ticker data with loading overlay."""
        if self.is_loading_ticker_data:
            return
        self.is_loading_ticker_data = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = DatabaseService()
            self.ticker_data = await service.get_ticker_data()
            self.ticker_data_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing ticker data: {e}")
        finally:
            self.is_loading_ticker_data = False
