import asyncio

import reflex as rx
from app.services import MarketDataService
from app.states.market_data.types import HistoricalDataItem


class HistoricalDataMixin(rx.State, mixin=True):
    """
    Mixin providing Historical Data state.
    """

    historical_data: list[HistoricalDataItem] = []
    is_loading_historical_data: bool = False
    historical_data_error: str = ""
    historical_data_last_updated: str = "—"
    historical_auto_refresh: bool = True  # Auto-refresh toggle

    historical_data_search: str = ""

    async def load_historical_data(self):
        self.is_loading_historical_data = True
        self.historical_data_error = ""
        try:
            service = MarketDataService()
            self.historical_data = await service.get_historical_data()
        except Exception as e:
            self.historical_data_error = str(e)
            import logging

            logging.exception(f"Error loading historical data: {e}")
        finally:
            self.is_loading_historical_data = False
            from datetime import datetime

            self.historical_data_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

    @rx.event(background=True)
    async def start_historical_auto_refresh(self):
        """Background task for Historical Data auto-refresh (5s interval)."""
        while True:
            async with self:
                if not self.historical_auto_refresh:
                    break
                self.simulate_historical_update()
            await asyncio.sleep(5)

    def toggle_historical_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.historical_auto_refresh = value
        if value:
            return type(self).start_historical_auto_refresh

    def simulate_historical_update(self):
        """Simulated delta update for demo - called by rx.moment interval."""
        if not self.historical_auto_refresh or len(self.historical_data) < 1:
            return

        import random
        from datetime import datetime

        # Update 1-3 random rows (less frequent for historical)
        for _ in range(random.randint(1, min(3, len(self.historical_data)))):
            idx = random.randint(0, len(self.historical_data) - 1)
            row = self.historical_data[idx]
            # Simulate price updates
            if "close" in row and row["close"]:
                row["close"] = round(
                    float(row["close"]) * random.uniform(0.99, 1.01), 2
                )
            if "high" in row and row["high"]:
                row["high"] = round(float(row["high"]) * random.uniform(0.99, 1.01), 2)
            if "low" in row and row["low"]:
                row["low"] = round(float(row["low"]) * random.uniform(0.99, 1.01), 2)

        self.historical_data_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_historical_data_search(self, query: str):
        self.historical_data_search = query

    @rx.var(cache=True)
    def filtered_historical_data(self) -> list[HistoricalDataItem]:
        data = self.historical_data
        if self.historical_data_search:
            query = self.historical_data_search.lower()
            data = [item for item in data if query in item.get("ticker", "").lower()]
        return data
