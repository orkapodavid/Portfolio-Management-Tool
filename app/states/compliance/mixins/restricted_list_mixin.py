"""Mixin for Restricted List grid state."""

import asyncio
from datetime import datetime

import reflex as rx
from app.services import ComplianceService
from app.states.compliance.types import RestrictedListItem
import logging

class RestrictedListMixin(rx.State, mixin=True):
    """
    Mixin providing Restricted List data state and filtering.
    """

    # Restricted List data
    restricted_list: list[RestrictedListItem] = []
    is_loading_restricted_list: bool = False
    restricted_list_last_updated: str = "—"

    async def load_restricted_list(self):
        """Load restricted list data from ComplianceService."""
        self.is_loading_restricted_list = True
        try:
            service = ComplianceService()
            self.restricted_list = await service.get_restricted_list()
            self.restricted_list_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error loading restricted list: {e}")
        finally:
            self.is_loading_restricted_list = False

    async def force_refresh_restricted_list(self):
        """Force refresh restricted list data with loading overlay."""
        if self.is_loading_restricted_list:
            return  # Debounce: ignore clicks while loading
        self.is_loading_restricted_list = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.3)  # Brief delay for loading overlay
        try:
            service = ComplianceService()
            self.restricted_list = await service.get_restricted_list()
            self.restricted_list_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error refreshing restricted list: {e}")
        finally:
            self.is_loading_restricted_list = False

    @rx.var(cache=True)
    def filtered_restricted_list(self) -> list[RestrictedListItem]:
        """Filtered restricted list based on search query."""
        if not self.current_search_query:
            return self.restricted_list

        query = self.current_search_query.lower()
        return [
            item
            for item in self.restricted_list
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
        ]
