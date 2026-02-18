import asyncio

import reflex as rx
from app.services import RiskService
from app.states.risk.types import RiskInputItem
import logging
import random

class RiskInputsMixin(rx.State, mixin=True):
    """
    Mixin providing Risk Inputs data state and filtering.
    """

    # Risk Inputs data
    risk_inputs: list[RiskInputItem] = []
    is_loading_risk_inputs: bool = False
    risk_inputs_error: str = ""
    risk_inputs_last_updated: str = "—"
    risk_inputs_auto_refresh: bool = True

    # Filters
    risk_inputs_search: str = ""
    risk_inputs_sort_column: str = ""
    risk_inputs_sort_direction: str = "asc"

    async def load_risk_inputs_data(self):
        """Load Risk Inputs data from RiskService."""
        self.is_loading_risk_inputs = True
        self.risk_inputs_error = ""
        try:
            service = RiskService()
            self.risk_inputs = await service.get_risk_inputs()
        except Exception as e:
            self.risk_inputs_error = str(e)

            logging.exception(f"Error loading risk inputs data: {e}")
        finally:
            self.is_loading_risk_inputs = False
            from datetime import datetime

            self.risk_inputs_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @rx.event(background=True)
    async def start_risk_inputs_auto_refresh(self):
        """Background task for Risk Inputs auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.risk_inputs_auto_refresh:
                    break
                self.simulate_risk_inputs_update()
            await asyncio.sleep(2)

    def toggle_risk_inputs_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.risk_inputs_auto_refresh = value
        if value:
            return type(self).start_risk_inputs_auto_refresh

    def simulate_risk_inputs_update(self):
        """Simulated delta update for demo - random risk input fluctuations."""
        if not self.risk_inputs_auto_refresh or len(self.risk_inputs) < 1:
            return

        from datetime import datetime

        # Create a new list to trigger change detection
        new_list = list(self.risk_inputs)

        # Update 1-3 random rows
        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            # Create a new row dict (immutable update for AG Grid change detection)
            new_row = dict(old_row)

            # Simulate small changes on numeric fields
            for field in ["spot_price", "volatility", "interest_rate", "dividend_yield"]:
                if field in new_row and new_row[field] is not None:
                    try:
                        val = float(new_row[field])
                        new_row[field] = round(val * random.uniform(0.99, 1.01), 4)
                    except (ValueError, TypeError):
                        pass

            new_list[idx] = new_row

        self.risk_inputs = new_list
        self.risk_inputs_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_risk_inputs_search(self, query: str):
        self.risk_inputs_search = query

    @rx.var(cache=True)
    def filtered_risk_inputs(self) -> list[RiskInputItem]:
        data = self.risk_inputs
        # Filter
        if self.risk_inputs_search:
            query = self.risk_inputs_search.lower()
            data = [
                item
                for item in data
                if query in item.get("ticker", "").lower()
                or query in item.get("underlying", "").lower()
            ]
        return data
