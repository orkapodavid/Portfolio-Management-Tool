import asyncio
from datetime import datetime

import reflex as rx
from app.states.risk.types import RiskMeasureItem
import logging
import random
from app.services import services

class RiskMeasuresMixin(rx.State, mixin=True):
    """
    Mixin providing Risk Measures data state and filtering.
    """

    # Risk Measures data
    risk_measures: list[RiskMeasureItem] = []
    is_loading_risk_measures: bool = False
    risk_measures_error: str = ""
    risk_measures_last_updated: str = "—"
    risk_measures_auto_refresh: bool = True

    # Filters
    risk_measures_search: str = ""
    risk_measures_sort_column: str = ""
    risk_measures_sort_direction: str = "asc"

    # Position date — defaults to today
    risk_measures_position_date: str = ""

    def _ensure_risk_measures_date(self) -> str:
        """Return position_date or today if empty."""
        if not self.risk_measures_position_date:
            self.risk_measures_position_date = datetime.now().strftime("%Y-%m-%d")
        return self.risk_measures_position_date

    async def load_risk_measures_data(self):
        """Load Risk Measures data from RiskService."""
        self.is_loading_risk_measures = True
        self.risk_measures_error = ""
        try:
            pos_date = self._ensure_risk_measures_date()
            self.risk_measures = await services.risk.get_risk_measures(pos_date)
        except Exception as e:
            self.risk_measures_error = str(e)

            logging.exception(f"Error loading risk measures data: {e}")
        finally:
            self.is_loading_risk_measures = False
            self.risk_measures_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

    async def set_risk_measures_position_date(self, value: str):
        """Set position date and reload data."""
        self.risk_measures_position_date = value
        await self.load_risk_measures_data()

    async def force_refresh_risk_measures(self):
        """Force refresh risk measures data with loading overlay."""
        if self.is_loading_risk_measures:
            return  # Debounce
        self.is_loading_risk_measures = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.3)
        try:
            pos_date = self._ensure_risk_measures_date()
            self.risk_measures = await services.risk.get_risk_measures(pos_date)
            self.risk_measures_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error refreshing risk measures: {e}")
        finally:
            self.is_loading_risk_measures = False

    @rx.event(background=True)
    async def start_risk_measures_auto_refresh(self):
        """Background task for Risk Measures auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.risk_measures_auto_refresh:
                    break
                self.simulate_risk_measures_update()
            await asyncio.sleep(2)

    def toggle_risk_measures_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.risk_measures_auto_refresh = value
        if value:
            return type(self).start_risk_measures_auto_refresh

    def simulate_risk_measures_update(self):
        """Simulated delta update for demo - random risk measure fluctuations."""
        if not self.risk_measures_auto_refresh or len(self.risk_measures) < 1:
            return

        # Create a new list to trigger change detection
        new_list = list(self.risk_measures)

        # Update 1-3 random rows
        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            # Create a new row dict (immutable update for AG Grid change detection)
            new_row = dict(old_row)

            # Simulate small changes on numeric fields
            for field in ["spot_price", "fx_rate", "delta", "gamma", "vega", "theta"]:
                if field in new_row and new_row[field] is not None:
                    try:
                        val = float(new_row[field])
                        new_row[field] = round(val * random.uniform(0.99, 1.01), 4)
                    except (ValueError, TypeError):
                        pass

            new_list[idx] = new_row

        self.risk_measures = new_list
        self.risk_measures_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_risk_measures_search(self, query: str):
        self.risk_measures_search = query

    @rx.var(cache=True)
    def filtered_risk_measures(self) -> list[RiskMeasureItem]:
        data = self.risk_measures
        # Filter
        if self.risk_measures_search:
            query = self.risk_measures_search.lower()
            data = [
                item
                for item in data
                if query in item.get("ticker", "").lower()
                or query in item.get("underlying", "").lower()
            ]
        return data
