import asyncio

import reflex as rx
from app.states.market_data.types import FXDataItem
import logging
import random
from app.services import services

class FXDataMixin(rx.State, mixin=True):
    """
    Mixin providing FX Data state.
    """

    fx_data: list[FXDataItem] = []
    is_loading_fx_data: bool = False
    fx_data_error: str = ""
    fx_data_last_updated: str = "—"
    fx_auto_refresh: bool = True  # Auto-refresh toggle

    fx_data_search: str = ""

    async def load_fx_data(self):
        self.is_loading_fx_data = True
        self.fx_data_error = ""
        try:
            self.fx_data = await services.market_data.get_fx_data()
        except Exception as e:
            self.fx_data_error = str(e)

            logging.exception(f"Error loading FX data: {e}")
        finally:
            self.is_loading_fx_data = False
            from datetime import datetime

            self.fx_data_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @rx.event(background=True)
    async def start_fx_auto_refresh(self):
        """Background task for FX Data auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.fx_auto_refresh:
                    break
                self.simulate_fx_update()
            await asyncio.sleep(2)

    def toggle_fx_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.fx_auto_refresh = value
        if value:
            return type(self).start_fx_auto_refresh

    def simulate_fx_update(self):
        """Simulated delta update for demo - called by rx.moment interval."""
        if not self.fx_auto_refresh or len(self.fx_data) < 1:
            return

        from datetime import datetime

        # Update 1-5 random rows with price fluctuations
        for _ in range(random.randint(1, min(5, len(self.fx_data)))):
            idx = random.randint(0, len(self.fx_data) - 1)
            row = self.fx_data[idx]
            # Simulate small price changes
            if "last_price" in row and row["last_price"]:
                row["last_price"] = round(
                    float(row["last_price"]) * random.uniform(0.999, 1.001), 5
                )
            if "bid" in row and row["bid"]:
                row["bid"] = round(
                    float(row["bid"]) * random.uniform(0.999, 1.001), 5
                )
            if "ask" in row and row["ask"]:
                row["ask"] = round(
                    float(row["ask"]) * random.uniform(0.999, 1.001), 5
                )

        self.fx_data_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_fx_data_search(self, query: str):
        self.fx_data_search = query

    @rx.var(cache=True)
    def filtered_fx_data(self) -> list[FXDataItem]:
        data = self.fx_data
        if self.fx_data_search:
            query = self.fx_data_search.lower()
            data = [item for item in data if query in item.get("pair", "").lower()]
        return data
