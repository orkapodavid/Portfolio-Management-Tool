"""Mixin for Monthly Exercise Limit grid state."""

import asyncio
from datetime import datetime

import reflex as rx
from app.services import ComplianceService
from app.states.compliance.types import MonthlyExerciseLimitItem
import logging

class MonthlyExerciseLimitMixin(rx.State, mixin=True):
    """
    Mixin providing Monthly Exercise Limit data state and filtering.
    """

    # Monthly Exercise Limit data
    monthly_exercise_limit: list[MonthlyExerciseLimitItem] = []
    is_loading_monthly_exercise_limit: bool = False
    monthly_exercise_limit_last_updated: str = "—"
    monthly_exercise_limit_position_date: str = ""

    async def set_monthly_exercise_limit_position_date(self, value: str):
        """Set position date and reload data."""
        self.monthly_exercise_limit_position_date = value
        yield
        await self.load_monthly_exercise_limit()

    async def load_monthly_exercise_limit(self):
        """Load monthly exercise limit data from ComplianceService."""
        self.is_loading_monthly_exercise_limit = True
        try:
            service = ComplianceService()
            self.monthly_exercise_limit = await service.get_monthly_exercise_limit(self.monthly_exercise_limit_position_date)
            self.monthly_exercise_limit_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error loading monthly exercise limit: {e}")
        finally:
            self.is_loading_monthly_exercise_limit = False

    async def force_refresh_monthly_exercise_limit(self):
        """Force refresh monthly exercise limit data with loading overlay."""
        if self.is_loading_monthly_exercise_limit:
            return  # Debounce: ignore clicks while loading
        self.is_loading_monthly_exercise_limit = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.3)  # Brief delay for loading overlay
        try:
            service = ComplianceService()
            self.monthly_exercise_limit = await service.get_monthly_exercise_limit(self.monthly_exercise_limit_position_date)
            self.monthly_exercise_limit_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error refreshing monthly exercise limit: {e}")
        finally:
            self.is_loading_monthly_exercise_limit = False

    @rx.var(cache=True)
    def filtered_monthly_exercise_limit(self) -> list[MonthlyExerciseLimitItem]:
        """Filtered monthly exercise limit based on search query."""
        if not self.current_search_query:
            return self.monthly_exercise_limit

        query = self.current_search_query.lower()
        return [
            item
            for item in self.monthly_exercise_limit
            if query in item.get("ticker", "").lower()
            or query in item.get("underlying", "").lower()
        ]
