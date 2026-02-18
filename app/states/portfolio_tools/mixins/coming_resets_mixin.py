"""
Coming Resets Mixin - Tab-specific state for Coming Resets data.

Provides auto-refresh background task and force refresh functionality.
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.services import PortfolioToolsService
from app.states.portfolio_tools.types import ComingResetItem
import logging
import random

class ComingResetsMixin(rx.State, mixin=True):
    """
    Mixin providing Coming Resets data state with auto-refresh.
    """

    # Coming Resets data
    coming_resets: list[ComingResetItem] = []
    is_loading_coming_resets: bool = False
    coming_resets_last_updated: str = "—"
    coming_resets_auto_refresh: bool = True

    async def load_coming_resets_data(self):
        """Load Coming Resets data from PortfolioToolsService."""
        self.is_loading_coming_resets = True
        try:
            service = PortfolioToolsService()
            self.coming_resets = await service.get_coming_resets()
            self.coming_resets_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error loading coming resets data: {e}")
        finally:
            self.is_loading_coming_resets = False

    @rx.event(background=True)
    async def start_coming_resets_auto_refresh(self):
        """Background task for Coming Resets auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.coming_resets_auto_refresh:
                    break
                self.simulate_coming_resets_update()
            await asyncio.sleep(2)

    def toggle_coming_resets_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.coming_resets_auto_refresh = value
        if value:
            return type(self).start_coming_resets_auto_refresh

    def simulate_coming_resets_update(self):
        """Simulated delta update for demo - random day count changes."""
        if not self.coming_resets_auto_refresh or len(self.coming_resets) < 1:
            return

        new_list = list(self.coming_resets)

        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            new_row = dict(old_row)

            # Simulate cal_days changes (countdown)
            if "cal_days" in new_row and new_row["cal_days"]:
                try:
                    val = int(str(new_row["cal_days"]))
                    if val > 0:
                        new_row["cal_days"] = str(val - random.randint(0, 1))
                except (ValueError, TypeError):
                    pass

            new_list[idx] = new_row

        self.coming_resets = new_list
        self.coming_resets_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_coming_resets(self):
        """Force refresh coming resets data with loading overlay."""
        if self.is_loading_coming_resets:
            return
        self.is_loading_coming_resets = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = PortfolioToolsService()
            self.coming_resets = await service.get_coming_resets()
            self.coming_resets_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        finally:
            self.is_loading_coming_resets = False
