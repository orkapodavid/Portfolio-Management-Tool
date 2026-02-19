"""Mixin for Beneficial Ownership grid state."""

import asyncio
from datetime import datetime

import reflex as rx
from app.states.compliance.types import BeneficialOwnershipItem
import logging
from app.services import services

class BeneficialOwnershipMixin(rx.State, mixin=True):
    """
    Mixin providing Beneficial Ownership data state and filtering.
    """

    # Beneficial Ownership data
    beneficial_ownership: list[BeneficialOwnershipItem] = []
    is_loading_beneficial_ownership: bool = False
    beneficial_ownership_last_updated: str = "—"
    beneficial_ownership_position_date: str = ""

    async def set_beneficial_ownership_position_date(self, value: str):
        """Set position date and reload data."""
        self.beneficial_ownership_position_date = value
        yield
        await self.load_beneficial_ownership()

    async def load_beneficial_ownership(self):
        """Load beneficial ownership data from ComplianceService."""
        self.is_loading_beneficial_ownership = True
        try:
            self.beneficial_ownership = await services.compliance.get_beneficial_ownership(self.beneficial_ownership_position_date)
            self.beneficial_ownership_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error loading beneficial ownership: {e}")
        finally:
            self.is_loading_beneficial_ownership = False

    async def force_refresh_beneficial_ownership(self):
        """Force refresh beneficial ownership data with loading overlay."""
        if self.is_loading_beneficial_ownership:
            return  # Debounce: ignore clicks while loading
        self.is_loading_beneficial_ownership = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.3)  # Brief delay for loading overlay
        try:
            self.beneficial_ownership = await services.compliance.get_beneficial_ownership(self.beneficial_ownership_position_date)
            self.beneficial_ownership_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error refreshing beneficial ownership: {e}")
        finally:
            self.is_loading_beneficial_ownership = False

    @rx.var(cache=True)
    def filtered_beneficial_ownership(self) -> list[BeneficialOwnershipItem]:
        """Filtered beneficial ownership based on search query."""
        # Access parent's search query
        if not self.current_search_query:
            return self.beneficial_ownership

        query = self.current_search_query.lower()
        return [
            item
            for item in self.beneficial_ownership
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
        ]
