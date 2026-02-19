"""
Special Terms Mixin - Tab-specific state for Special Terms data.

Provides auto-refresh background task and force refresh functionality.
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.states.instruments.types import SpecialTermItem
import logging
import random
from app.services import services

class SpecialTermsMixin(rx.State, mixin=True):
    """
    Mixin providing Special Terms data state with auto-refresh.
    """

    # Special Terms data
    special_terms: list[SpecialTermItem] = []
    is_loading_special_terms: bool = False
    special_terms_last_updated: str = "—"
    special_terms_auto_refresh: bool = True

    # Position date — defaults to today
    special_terms_position_date: str = ""

    def _ensure_special_terms_date(self) -> str:
        """Return position_date or today if empty."""
        if not self.special_terms_position_date:
            self.special_terms_position_date = datetime.now().strftime("%Y-%m-%d")
        return self.special_terms_position_date

    async def load_special_terms_data(self):
        """Load Special Terms data from InstrumentsService."""
        self.is_loading_special_terms = True
        try:
            pos_date = self._ensure_special_terms_date()
            self.special_terms = await services.instruments.get_special_terms(pos_date)
            self.special_terms_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error loading special terms data: {e}")
        finally:
            self.is_loading_special_terms = False

    async def set_special_terms_position_date(self, value: str):
        """Set position date and reload data."""
        self.special_terms_position_date = value
        await self.load_special_terms_data()

    @rx.event(background=True)
    async def start_special_terms_auto_refresh(self):
        """Background task for Special Terms auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.special_terms_auto_refresh:
                    break
                self.simulate_special_terms_update()
            await asyncio.sleep(2)

    def toggle_special_terms_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.special_terms_auto_refresh = value
        if value:
            return type(self).start_special_terms_auto_refresh

    def simulate_special_terms_update(self):
        """Simulated delta update for demo - random position changes."""
        if not self.special_terms_auto_refresh or len(self.special_terms) < 1:
            return

        new_list = list(self.special_terms)

        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            new_row = dict(old_row)

            # Simulate position changes
            if "position" in new_row and new_row["position"]:
                try:
                    val = float(str(new_row["position"]).replace(",", ""))
                    new_val = int(val * random.uniform(0.98, 1.02))
                    new_row["position"] = f"{new_val:,}"
                except (ValueError, TypeError):
                    pass

            new_list[idx] = new_row

        self.special_terms = new_list
        self.special_terms_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_special_terms(self):
        """Force refresh special terms data with loading overlay."""
        if self.is_loading_special_terms:
            return
        self.is_loading_special_terms = True
        yield
        await asyncio.sleep(0.3)
        try:
            pos_date = self._ensure_special_terms_date()
            self.special_terms = await services.instruments.get_special_terms(pos_date)
            self.special_terms_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error refreshing special terms: {e}")
        finally:
            self.is_loading_special_terms = False
