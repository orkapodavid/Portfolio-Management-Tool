import reflex as rx
from app.states.market_data.mixins.market_data_mixin import MarketDataMixin
from app.states.market_data.mixins.fx_data_mixin import FXDataMixin
from app.states.market_data.mixins.historical_data_mixin import HistoricalDataMixin
from app.states.market_data.mixins.trading_calendar_mixin import TradingCalendarMixin
from app.states.market_data.mixins.market_hours_mixin import MarketHoursMixin
from app.states.market_data.mixins.ticker_data_mixin import TickerDataMixin


class MarketDataState(
    MarketDataMixin,
    FXDataMixin,
    HistoricalDataMixin,
    TradingCalendarMixin,
    MarketHoursMixin,
    TickerDataMixin,
    rx.State,
):
    """
    Main Market Data module state.
    """

    active_market_data_subtab: str = "Market Data"

    async def load_market_data_module_data(self):
        """Load data for the active subtab."""
        if self.active_market_data_subtab == "Market Data":
            await self.load_market_data()
        elif self.active_market_data_subtab == "FX Data":
            await self.load_fx_data()
        elif self.active_market_data_subtab == "Reference Data":
            await self.load_ticker_data()
        elif self.active_market_data_subtab == "Historical Data":
            await self.load_historical_data()
        elif self.active_market_data_subtab == "Trading Calendar":
            await self.load_trading_calendar()
        elif self.active_market_data_subtab == "Market Hours":
            await self.load_market_hours()

    def set_market_data_subtab(self, subtab: str):
        self.active_market_data_subtab = subtab
