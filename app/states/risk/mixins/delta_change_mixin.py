import asyncio
import logging
from datetime import datetime

import reflex as rx
from app.services import RiskService
from app.states.risk.types import DeltaChangeItem
from app.utils.simulation import simulate_numeric_tick

logger = logging.getLogger(__name__)


class DeltaChangeMixin(rx.State, mixin=True):
    """
    Mixin providing Delta Change data state and filtering.
    """

    # Delta Change data
    delta_changes: list[DeltaChangeItem] = []
    is_loading_delta_change: bool = False
    delta_change_error: str = ""
    delta_change_last_updated: str = "—"
    delta_change_auto_refresh: bool = True

    # Filters
    delta_change_search: str = ""
    delta_change_sort_column: str = ""
    delta_change_sort_direction: str = "asc"

    # Position date — defaults to today
    delta_change_position_date: str = ""

    def _ensure_delta_change_date(self) -> str:
        """Return position_date or today if empty."""
        if not self.delta_change_position_date:
            self.delta_change_position_date = datetime.now().strftime("%Y-%m-%d")
        return self.delta_change_position_date

    async def load_delta_change_data(self):
        """Load Delta Change data from RiskService."""
        self.is_loading_delta_change = True
        self.delta_change_error = ""
        try:
            pos_date = self._ensure_delta_change_date()
            service = RiskService()
            self.delta_changes = await service.get_delta_changes(pos_date)
        except Exception as e:
            self.delta_change_error = str(e)
            logger.exception(f"Error loading delta change data: {e}")
        finally:
            self.is_loading_delta_change = False
            self.delta_change_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

    async def set_delta_change_position_date(self, value: str):
        """Set position date and reload data."""
        self.delta_change_position_date = value
        await self.load_delta_change_data()

    async def force_refresh_delta_change(self):
        """Force refresh delta change data with loading overlay."""
        if self.is_loading_delta_change:
            return  # Debounce
        self.is_loading_delta_change = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.3)
        try:
            pos_date = self._ensure_delta_change_date()
            service = RiskService()
            self.delta_changes = await service.get_delta_changes(pos_date)
            self.delta_change_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            logger.exception(f"Error refreshing delta change: {e}")
        finally:
            self.is_loading_delta_change = False

    @rx.event(background=True)
    async def start_delta_change_auto_refresh(self):
        """Background task for Delta Change auto-refresh (2s interval).

        Uses while-True with guard clause. Max ~1 hour before auto-stop.
        """
        for _ in range(1800):  # Safety: max ~1 hour at 2s intervals
            async with self:
                if not self.delta_change_auto_refresh:
                    return
                self.simulate_delta_change_update()
            await asyncio.sleep(2)

    def toggle_delta_change_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.delta_change_auto_refresh = value
        if value:
            return type(self).start_delta_change_auto_refresh

    def simulate_delta_change_update(self):
        """Apply simulated tick using shared utility."""
        if not self.delta_change_auto_refresh or not self.delta_changes:
            return
        self.delta_changes = simulate_numeric_tick(
            rows=self.delta_changes,
            fields=["delta", "gamma", "vega", "theta"],
        )
        self.delta_change_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_delta_change_search(self, query: str):
        self.delta_change_search = query

    @rx.var(cache=True)
    def filtered_delta_changes(self) -> list[DeltaChangeItem]:
        data = self.delta_changes
        # Filter
        if self.delta_change_search:
            query = self.delta_change_search.lower()
            data = [
                item
                for item in data
                if query in item.get("ticker", "").lower()
                or query in item.get("company_name", "").lower()
            ]
        return data
