"""
Reset Dates Mixin - Tab-specific state for Reset Dates data.

Provides auto-refresh background task and force refresh functionality.
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.services import PortfolioToolsService
from app.states.portfolio_tools.types import ResetDateItem
import logging
import random

class ResetDatesMixin(rx.State, mixin=True):
    """
    Mixin providing Reset Dates data state with auto-refresh.
    """

    # Reset Dates data
    reset_dates: list[ResetDateItem] = []
    is_loading_reset_dates: bool = False
    reset_dates_last_updated: str = "—"
    reset_dates_auto_refresh: bool = True

    # Filter fields
    reset_dates_ticker: str = "4592 JP_Series 1"
    reset_dates_start_date: str = "2026-03-03"
    reset_dates_end_date: str = "2029-03-08"
    reset_dates_frequency: str = "semiannually"
    reset_dates_month: str = "3"
    reset_dates_day: str = "3"
    reset_dates_up_down: str = "up and down"

    def set_reset_dates_ticker(self, value: str):
        """Set ticker filter."""
        self.reset_dates_ticker = value

    def set_reset_dates_start_date(self, value: str):
        """Set start date filter."""
        self.reset_dates_start_date = value

    def set_reset_dates_end_date(self, value: str):
        """Set end date filter."""
        self.reset_dates_end_date = value

    def set_reset_dates_frequency(self, value: str):
        """Set frequency filter."""
        self.reset_dates_frequency = value

    def set_reset_dates_month(self, value: str):
        """Set month filter."""
        self.reset_dates_month = value

    def set_reset_dates_day(self, value: str):
        """Set day filter."""
        self.reset_dates_day = value

    def set_reset_dates_up_down(self, value: str):
        """Set up/down filter."""
        self.reset_dates_up_down = value

    async def apply_reset_dates_filters(self):
        """Apply filters and reload data."""
        self.is_loading_reset_dates = True
        yield
        await self.load_reset_dates_data()

    async def load_reset_dates_data(self):
        """Load Reset Dates data from PortfolioToolsService."""
        self.is_loading_reset_dates = True
        try:
            service = PortfolioToolsService()
            self.reset_dates = await service.get_reset_dates(
                ticker=self.reset_dates_ticker,
                start_date=self.reset_dates_start_date,
                end_date=self.reset_dates_end_date,
                frequency=self.reset_dates_frequency,
                reset_month=self.reset_dates_month,
                reset_day=self.reset_dates_day,
                reset_up_down=self.reset_dates_up_down,
            )
            self.reset_dates_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:

            logging.exception(f"Error loading reset dates data: {e}")
        finally:
            self.is_loading_reset_dates = False

    @rx.event(background=True)
    async def start_reset_dates_auto_refresh(self):
        """Background task for Reset Dates auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.reset_dates_auto_refresh:
                    break
                self.simulate_reset_dates_update()
            await asyncio.sleep(2)

    def toggle_reset_dates_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.reset_dates_auto_refresh = value
        if value:
            return type(self).start_reset_dates_auto_refresh

    def simulate_reset_dates_update(self):
        """Simulated delta update for demo - random price changes."""
        if not self.reset_dates_auto_refresh or len(self.reset_dates) < 1:
            return

        new_list = list(self.reset_dates)

        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            new_row = dict(old_row)

            # Simulate market_price changes
            if "market_price" in new_row and new_row["market_price"]:
                try:
                    val = float(str(new_row["market_price"]).replace(",", ""))
                    new_val = round(val * random.uniform(0.995, 1.005), 2)
                    new_row["market_price"] = f"{new_val:,.2f}"
                except (ValueError, TypeError):
                    pass

            new_list[idx] = new_row

        self.reset_dates = new_list
        self.reset_dates_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_reset_dates(self):
        """Force refresh reset dates data with loading overlay."""
        if self.is_loading_reset_dates:
            return
        self.is_loading_reset_dates = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = PortfolioToolsService()
            self.reset_dates = await service.get_reset_dates(
                ticker=self.reset_dates_ticker,
                start_date=self.reset_dates_start_date,
                end_date=self.reset_dates_end_date,
                frequency=self.reset_dates_frequency,
                reset_month=self.reset_dates_month,
                reset_day=self.reset_dates_day,
                reset_up_down=self.reset_dates_up_down,
            )
            self.reset_dates_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        finally:
            self.is_loading_reset_dates = False
