import asyncio

import reflex as rx
from app.services import RiskService
from app.states.risk.types import RiskMeasureItem


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

    async def load_risk_measures_data(self):
        """Load Risk Measures data from RiskService."""
        self.is_loading_risk_measures = True
        self.risk_measures_error = ""
        try:
            service = RiskService()
            self.risk_measures = await service.get_risk_measures()
        except Exception as e:
            self.risk_measures_error = str(e)
            import logging

            logging.exception(f"Error loading risk measures data: {e}")
        finally:
            self.is_loading_risk_measures = False
            from datetime import datetime

            self.risk_measures_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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

        import random
        from datetime import datetime

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
