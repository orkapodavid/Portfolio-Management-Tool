import reflex as rx
from app.services import MarketDataService
from app.states.market_data.types import TradingCalendarItem


class TradingCalendarMixin(rx.State, mixin=True):
    """
    Mixin providing Trading Calendar state.
    """

    trading_calendar: list[TradingCalendarItem] = []
    is_loading_trading_calendar: bool = False
    trading_calendar_error: str = ""

    async def load_trading_calendar(self):
        self.is_loading_trading_calendar = True
        self.trading_calendar_error = ""
        try:
            service = MarketDataService()
            self.trading_calendar = await service.get_trading_calendar()
        except Exception as e:
            self.trading_calendar_error = str(e)
            import logging

            logging.exception(f"Error loading trading calendar: {e}")
        finally:
            self.is_loading_trading_calendar = False
