"""
Market Data Mixin - State functionality for Market Data

This Mixin provides all market data-related state variables, computed vars,
and event handlers. It integrates with MarketDataService for data access.

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
Pattern: State Mixin for code reuse
"""

import reflex as rx
from app.services import MarketDataService
from app.states.dashboard.types import (
    MarketDataItem,
    FXDataItem,
    HistoricalDataItem,
    TradingCalendarItem,
    MarketHoursItem,
    TickerDataItem,
)


class MarketDataMixin(rx.State, mixin=True):
    """
    Mixin providing market data state and filtering.

    Data provided:
    - Market data
    - FX data
    - Historical data
    - Trading calendar
    - Market hours
    - Ticker/reference data
    """

    # Market data lists
    market_data: list[MarketDataItem] = []
    fx_data: list[FXDataItem] = []
    historical_data: list[HistoricalDataItem] = []
    trading_calendar: list[TradingCalendarItem] = []
    market_hours: list[MarketHoursItem] = []
    ticker_data: list[TickerDataItem] = []

    async def load_market_data(self):
        """Load all market data from MarketDataService."""
        try:
            service = MarketDataService()
            self.market_data = await service.get_market_data()
            self.fx_data = await service.get_fx_data()
            self.historical_data = await service.get_historical_data()
            self.trading_calendar = await service.get_trading_calendar()
            self.market_hours = await service.get_market_hours()
            self.ticker_data = await service.get_ticker_data()
        except Exception as e:
            import logging

            logging.exception(f"Error loading market data: {e}")
