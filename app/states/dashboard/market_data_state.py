"""
Market Data State - Portfolio Dashboard Substate

Handles all market data for the portfolio dashboard.

This follows Reflex best practices for state architecture:
- Focused responsibility (only market data)
- Service integration (uses MarketDataService)
- Independent from other dashboard states
- Efficient loading (only loads when needed)

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
Pattern: Flat state structure with focused substates

Created as part of portfolio_dashboard_state.py restructuring.
"""

import reflex as rx
from app.services import MarketDataService


class MarketDataState(rx.State):
    """
    State management for real-time market data.

    Responsibilities:
    - Load real-time market data for tracked securities
    - Handle market data updates/refreshes
    - Provide FX rates
    - Handle filtering and search for market data view

    Best Practices Applied:
    1. Single Responsibility: Only handles market data
    2. Service Integration: Uses MarketDataService for data access
    3. Independent State: Doesn't inherit from other states
    4. Async Loading: Loads data asynchronously on demand
    """

    # Data storage
    market_data: list[dict] = []  # Real-time market data
    fx_rates: list[dict] = []  # FX rates

    # UI state
    is_loading: bool = False
    current_search_query: str = ""
    auto_refresh_enabled: bool = False
    last_refresh_time: str = ""

    async def on_load(self):
        """
        Called when Market Data view loads.

        Best Practice: Use on_load for initial data fetching.
        """
        await self.load_market_data()

    async def load_market_data(self):
        """
        Load market data from MarketDataService.

        Service Integration Pattern:
        1. Set loading state
        2. Instantiate service
        3. Call service methods
        4. Update state with results
        5. Clear loading state
        """
        self.is_loading = True
        try:
            service = MarketDataService()

            # Get list of tickers to track (could come from positions)
            # For now using example tickers
            tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "NVDA"]

            # Load real-time market data
            self.market_data = await service.get_realtime_market_data(tickers)

            # Load FX rates
            fx_pairs = ["EURUSD", "GBPUSD", "USDJPY"]
            self.fx_rates = await service.get_fx_rates(fx_pairs)

            # Update last refresh time
            from datetime import datetime

            self.last_refresh_time = datetime.now().strftime("%H:%M:%S")

        except Exception as e:
            import logging

            logging.exception(f"Error loading market data: {e}")
        finally:
            self.is_loading = False

    @rx.event
    async def refresh_market_data(self):
        """
        Manually refresh market data.

        User can trigger this to get latest prices.
        """
        await self.load_market_data()
        yield rx.toast("Market data refreshed", position="bottom-right")

    @rx.event
    def set_search_query(self, query: str):
        """Update search query for filtering."""
        self.current_search_query = query

    @rx.event
    def toggle_auto_refresh(self):
        """Toggle auto-refresh mode."""
        self.auto_refresh_enabled = not self.auto_refresh_enabled

    @rx.var(cache=True)
    def filtered_market_data(self) -> list[dict]:
        """Filtered market data based on search query."""
        if not self.current_search_query:
            return self.market_data

        query = self.current_search_query.lower()
        return [
            item for item in self.market_data if query in item.get("ticker", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_fx_rates(self) -> list[dict]:
        """Filtered FX rates based on search query."""
        if not self.current_search_query:
            return self.fx_rates

        query = self.current_search_query.lower()
        return [
            item for item in self.fx_rates if query in item.get("ticker", "").lower()
        ]

    @rx.var
    def is_market_open(self) -> bool:
        """
        Check if market is currently open.

        Simplified check - real implementation would check actual market hours.
        """
        # TODO: Implement proper market hours check
        return True
