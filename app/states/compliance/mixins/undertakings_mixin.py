"""Mixin for Undertakings grid state."""

import asyncio
from datetime import datetime

import reflex as rx
from app.services import ComplianceService
from app.states.compliance.types import UndertakingItem
import logging

class UndertakingsMixin(rx.State, mixin=True):
    """
    Mixin providing Undertakings data state and filtering.
    """

    # Undertakings data
    undertakings: list[UndertakingItem] = []
    is_loading_undertakings: bool = False
    undertakings_last_updated: str = "—"
    undertakings_position_date: str = ""

    async def set_undertakings_position_date(self, value: str):
        """Set position date and reload data."""
        self.undertakings_position_date = value
        yield
        await self.load_undertakings()

    async def load_undertakings(self):
        """Load undertakings data from ComplianceService."""
        self.is_loading_undertakings = True
        try:
            service = ComplianceService()
            self.undertakings = await service.get_undertakings(self.undertakings_position_date)
            self.undertakings_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error loading undertakings: {e}")
        finally:
            self.is_loading_undertakings = False

    async def force_refresh_undertakings(self):
        """Force refresh undertakings data with loading overlay."""
        if self.is_loading_undertakings:
            return  # Debounce: ignore clicks while loading
        self.is_loading_undertakings = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.3)  # Brief delay for loading overlay
        try:
            service = ComplianceService()
            self.undertakings = await service.get_undertakings(self.undertakings_position_date)
            self.undertakings_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error refreshing undertakings: {e}")
        finally:
            self.is_loading_undertakings = False

    @rx.var(cache=True)
    def filtered_undertakings(self) -> list[UndertakingItem]:
        """Filtered undertakings based on search query."""
        if not self.current_search_query:
            return self.undertakings

        query = self.current_search_query.lower()
        return [
            item
            for item in self.undertakings
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
            or query in item.get("deal_num", "").lower()
        ]
