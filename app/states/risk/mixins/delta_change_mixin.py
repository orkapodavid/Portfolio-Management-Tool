import asyncio
from datetime import datetime

import reflex as rx
from app.services import RiskService
from app.states.risk.types import DeltaChangeItem


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
            import logging

            logging.exception(f"Error loading delta change data: {e}")
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
            import logging

            logging.exception(f"Error refreshing delta change: {e}")
        finally:
            self.is_loading_delta_change = False

    @rx.event(background=True)
    async def start_delta_change_auto_refresh(self):
        """Background task for Delta Change auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.delta_change_auto_refresh:
                    break
                self.simulate_delta_change_update()
            await asyncio.sleep(2)

    def toggle_delta_change_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.delta_change_auto_refresh = value
        if value:
            return type(self).start_delta_change_auto_refresh

    def simulate_delta_change_update(self):
        """Simulated delta update for demo - random risk fluctuations."""
        if not self.delta_change_auto_refresh or len(self.delta_changes) < 1:
            return

        import random

        # Create a new list to trigger change detection
        new_list = list(self.delta_changes)

        # Update 1-3 random rows
        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            # Create a new row dict (immutable update for AG Grid change detection)
            new_row = dict(old_row)

            # Simulate small changes on Greek fields
            for field in ["delta", "gamma", "vega", "theta"]:
                if field in new_row and new_row[field] is not None:
                    try:
                        val = float(new_row[field])
                        new_row[field] = round(val * random.uniform(0.98, 1.02), 4)
                    except (ValueError, TypeError):
                        pass

            new_list[idx] = new_row

        self.delta_changes = new_list
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
