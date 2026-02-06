"""
Short ECL Mixin - Tab-specific state for Short ECL data.

Provides auto-refresh background task and force refresh functionality.
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.services import PortfolioToolsService
from app.states.portfolio_tools.types import ShortECLItem


class ShortECLMixin(rx.State, mixin=True):
    """
    Mixin providing Short ECL data state with auto-refresh.
    """

    # Short ECL data
    short_ecl: list[ShortECLItem] = []
    is_loading_short_ecl: bool = False
    short_ecl_last_updated: str = "—"
    short_ecl_auto_refresh: bool = True

    async def load_short_ecl_data(self):
        """Load Short ECL data from PortfolioToolsService."""
        self.is_loading_short_ecl = True
        try:
            service = PortfolioToolsService()
            self.short_ecl = await service.get_short_ecl()
            self.short_ecl_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            import logging

            logging.exception(f"Error loading short ECL data: {e}")
        finally:
            self.is_loading_short_ecl = False

    @rx.event(background=True)
    async def start_short_ecl_auto_refresh(self):
        """Background task for Short ECL auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.short_ecl_auto_refresh:
                    break
                self.simulate_short_ecl_update()
            await asyncio.sleep(2)

    def toggle_short_ecl_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.short_ecl_auto_refresh = value
        if value:
            return type(self).start_short_ecl_auto_refresh

    def simulate_short_ecl_update(self):
        """Simulated delta update for demo - random short position changes."""
        if not self.short_ecl_auto_refresh or len(self.short_ecl) < 1:
            return

        import random

        new_list = list(self.short_ecl)

        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            new_row = dict(old_row)

            # Simulate short_position changes
            if "short_position" in new_row and new_row["short_position"]:
                try:
                    val = float(str(new_row["short_position"]).replace(",", ""))
                    new_val = int(val * random.uniform(0.98, 1.02))
                    new_row["short_position"] = f"{new_val:,}"
                except (ValueError, TypeError):
                    pass

            new_list[idx] = new_row

        self.short_ecl = new_list
        self.short_ecl_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_short_ecl(self):
        """Force refresh short ECL data with loading overlay."""
        if self.is_loading_short_ecl:
            return
        self.is_loading_short_ecl = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = PortfolioToolsService()
            self.short_ecl = await service.get_short_ecl()
            self.short_ecl_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        finally:
            self.is_loading_short_ecl = False
