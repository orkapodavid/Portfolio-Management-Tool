"""
Instrument Data Mixin - Tab-specific state for Instrument Data.

Provides auto-refresh background task and force refresh functionality.
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.states.instruments.types import InstrumentDataItem
import logging
import random
from app.services import services

class InstrumentDataMixin(rx.State, mixin=True):
    """
    Mixin providing Instrument Data state with auto-refresh.
    """

    # Instrument Data
    instrument_data: list[InstrumentDataItem] = []
    is_loading_instrument_data: bool = False
    instrument_data_last_updated: str = "—"
    instrument_data_auto_refresh: bool = True

    async def load_instrument_data(self):
        """Load Instrument Data from InstrumentsService."""
        self.is_loading_instrument_data = True
        try:
            self.instrument_data = await services.instruments.get_instrument_data()
            self.instrument_data_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error loading instrument data: {e}")
        finally:
            self.is_loading_instrument_data = False

    @rx.event(background=True)
    async def start_instrument_data_auto_refresh(self):
        """Background task for Instrument Data auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.instrument_data_auto_refresh:
                    break
                self.simulate_instrument_data_update()
            await asyncio.sleep(2)

    def toggle_instrument_data_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.instrument_data_auto_refresh = value
        if value:
            return type(self).start_instrument_data_auto_refresh

    def simulate_instrument_data_update(self):
        """Simulated delta update for demo - update timestamps."""
        if not self.instrument_data_auto_refresh or len(self.instrument_data) < 1:
            return

        new_list = list(self.instrument_data)

        # Just trigger change detection by updating a few rows
        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            new_row = dict(old_row)
            new_list[idx] = new_row

        self.instrument_data = new_list
        self.instrument_data_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_instrument_data(self):
        """Force refresh instrument data with loading overlay."""
        if self.is_loading_instrument_data:
            return
        self.is_loading_instrument_data = True
        yield
        await asyncio.sleep(0.3)
        try:
            self.instrument_data = await services.instruments.get_instrument_data()
            self.instrument_data_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error refreshing instrument data: {e}")
        finally:
            self.is_loading_instrument_data = False
