import asyncio

import reflex as rx
from app.services import MarketDataService
from app.states.market_data.types import MarketDataItem


class MarketDataMixin(rx.State, mixin=True):
    """
    Mixin providing Market Data state.
    """

    market_data: list[MarketDataItem] = []
    is_loading_market_data: bool = False
    market_data_error: str = ""
    market_data_last_updated: str = "—"
    market_data_auto_refresh: bool = True  # Auto-refresh toggle

    market_data_search: str = ""

    async def load_market_data(self):
        self.is_loading_market_data = True
        self.market_data_error = ""
        try:
            service = MarketDataService()
            self.market_data = await service.get_market_data()
        except Exception as e:
            self.market_data_error = str(e)
            import logging

            logging.exception(f"Error loading market data: {e}")
        finally:
            self.is_loading_market_data = False
            from datetime import datetime

            self.market_data_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @rx.event(background=True)
    async def start_market_data_auto_refresh(self):
        """Background task for Market Data auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.market_data_auto_refresh:
                    break
                self.simulate_market_data_update()
            await asyncio.sleep(2)

    def toggle_market_data_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.market_data_auto_refresh = value
        if value:
            return type(self).start_market_data_auto_refresh

    def simulate_market_data_update(self):
        """Simulated delta update for demo - called by rx.moment interval."""
        if not self.market_data_auto_refresh or len(self.market_data) < 1:
            return

        import random
        from datetime import datetime

        # Update 1-5 random rows with price fluctuations
        for _ in range(random.randint(1, min(5, len(self.market_data)))):
            idx = random.randint(0, len(self.market_data) - 1)
            row = self.market_data[idx]
            # Simulate price/change updates
            if "last_price" in row and row["last_price"]:
                row["last_price"] = round(
                    float(row["last_price"]) * random.uniform(0.99, 1.01), 2
                )
            if "change" in row:
                row["change"] = round(random.uniform(-5, 5), 2)
            if "volume" in row and row["volume"]:
                row["volume"] = int(float(row["volume"]) * random.uniform(0.98, 1.02))

        self.market_data_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def set_market_data_search(self, query: str):
        self.market_data_search = query

    @rx.var(cache=True)
    def filtered_market_data(self) -> list[MarketDataItem]:
        data = self.market_data
        if self.market_data_search:
            query = self.market_data_search.lower()
            data = [
                item
                for item in data
                if query in item.get("ticker", "").lower()
                or query in item.get("description", "").lower()
            ]
        return data
