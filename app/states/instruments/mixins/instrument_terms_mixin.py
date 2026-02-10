"""
Instrument Terms Mixin - Tab-specific state for Instrument Terms data.

Provides auto-refresh background task and force refresh functionality.
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.services import InstrumentsService
from app.states.instruments.types import InstrumentTermItem


class InstrumentTermsMixin(rx.State, mixin=True):
    """
    Mixin providing Instrument Terms data state with auto-refresh.
    """

    # Instrument Terms data
    instrument_terms: list[InstrumentTermItem] = []
    is_loading_instrument_terms: bool = False
    instrument_terms_last_updated: str = "—"
    instrument_terms_auto_refresh: bool = True

    async def load_instrument_terms_data(self):
        """Load Instrument Terms data from InstrumentsService."""
        self.is_loading_instrument_terms = True
        try:
            service = InstrumentsService()
            self.instrument_terms = await service.get_instrument_terms()
            self.instrument_terms_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error loading instrument terms data: {e}")
        finally:
            self.is_loading_instrument_terms = False

    @rx.event(background=True)
    async def start_instrument_terms_auto_refresh(self):
        """Background task for Instrument Terms auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.instrument_terms_auto_refresh:
                    break
                self.simulate_instrument_terms_update()
            await asyncio.sleep(2)

    def toggle_instrument_terms_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.instrument_terms_auto_refresh = value
        if value:
            return type(self).start_instrument_terms_auto_refresh

    def simulate_instrument_terms_update(self):
        """Simulated delta update for demo - update timestamps."""
        if not self.instrument_terms_auto_refresh or len(self.instrument_terms) < 1:
            return

        import random

        new_list = list(self.instrument_terms)

        # Just trigger change detection by updating a few rows
        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            new_row = dict(old_row)
            new_list[idx] = new_row

        self.instrument_terms = new_list
        self.instrument_terms_last_updated = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    async def force_refresh_instrument_terms(self):
        """Force refresh instrument terms data with loading overlay."""
        if self.is_loading_instrument_terms:
            return
        self.is_loading_instrument_terms = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = InstrumentsService()
            self.instrument_terms = await service.get_instrument_terms()
            self.instrument_terms_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing instrument terms: {e}")
        finally:
            self.is_loading_instrument_terms = False
