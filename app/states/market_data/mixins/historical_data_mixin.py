import asyncio
from datetime import datetime

import reflex as rx
from app.services import MarketDataService
from app.states.market_data.types import HistoricalDataItem


class HistoricalDataMixin(rx.State, mixin=True):
    """
    Mixin providing Historical Data state.

    On every filter change the service is queried with the current parameters.
    Results are cached at the service level since historical data is immutable.
    """

    historical_data: list[HistoricalDataItem] = []
    is_loading_historical_data: bool = False
    historical_data_error: str = ""
    historical_data_last_updated: str = "—"
    historical_auto_refresh: bool = True  # Auto-refresh toggle

    historical_data_search: str = ""

    # --- Filter state ---
    historical_available_tickers: list[str] = []
    historical_selected_tickers: list[str] = []
    historical_from_date: str = ""
    historical_to_date: str = ""

    async def load_historical_data(self):
        """Load historical data using current filter params via the service."""
        self.is_loading_historical_data = True
        self.historical_data_error = ""
        try:
            service = MarketDataService()
            self.historical_data = await service.get_historical_data(
                tickers=self.historical_selected_tickers or None,
                start_date=self.historical_from_date or None,
                end_date=self.historical_to_date or None,
            )
            # Populate available tickers (query without filters to get all)
            if not self.historical_available_tickers:
                all_data = await service.get_historical_data()
                tickers = sorted(
                    set(
                        item.get("ticker", "")
                        for item in all_data
                        if item.get("ticker")
                    )
                )
                self.historical_available_tickers = tickers
        except Exception as e:
            self.historical_data_error = str(e)
            import logging

            logging.exception(f"Error loading historical data: {e}")
        finally:
            self.is_loading_historical_data = False
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

    # --- Filter event handlers ---

    async def toggle_historical_ticker(self, ticker: str):
        """Add or remove a ticker from the selection, then re-query."""
        if ticker in self.historical_selected_tickers:
            self.historical_selected_tickers = [
                t for t in self.historical_selected_tickers if t != ticker
            ]
        else:
            self.historical_selected_tickers = [
                *self.historical_selected_tickers,
                ticker,
            ]
        await self.load_historical_data()

    async def select_all_historical_tickers(self):
        """Select all available tickers and re-query."""
        self.historical_selected_tickers = list(self.historical_available_tickers)
        await self.load_historical_data()

    async def clear_historical_tickers(self):
        """Clear all selected tickers and re-query."""
        self.historical_selected_tickers = []
        await self.load_historical_data()

    async def set_historical_from_date(self, value: str):
        """Set the from-date filter and re-query."""
        self.historical_from_date = value
        await self.load_historical_data()

    async def set_historical_to_date(self, value: str):
        """Set the to-date filter and re-query."""
        self.historical_to_date = value
        await self.load_historical_data()

    async def apply_historical_filters(self):
        """Explicitly re-query with current filters."""
        await self.load_historical_data()

    async def clear_historical_filters(self):
        """Reset all filters to defaults and re-query."""
        self.historical_selected_tickers = []
        self.historical_from_date = ""
        self.historical_to_date = ""
        await self.load_historical_data()

    @rx.var(cache=True)
    def filtered_historical_data(self) -> list[HistoricalDataItem]:
        """Return data — filtering is done at the service level now.
        Only the quick-search toolbar filter is applied here."""
        data = self.historical_data
        if self.historical_data_search:
            query = self.historical_data_search.lower()
            data = [item for item in data if query in item.get("ticker", "").lower()]
        return data

    @rx.var(cache=True)
    def historical_selected_ticker_count(self) -> int:
        """Number of currently selected tickers."""
        return len(self.historical_selected_tickers)

    @rx.var(cache=True)
    def historical_has_active_filters(self) -> bool:
        """Whether any filters are currently active."""
        return bool(
            self.historical_selected_tickers
            or self.historical_from_date
            or self.historical_to_date
        )
