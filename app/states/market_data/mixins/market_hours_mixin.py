import reflex as rx
from app.services import MarketDataService
from app.states.market_data.types import MarketHoursItem


class MarketHoursMixin(rx.State, mixin=True):
    """
    Mixin providing Market Hours state.
    """

    market_hours: list[MarketHoursItem] = []
    is_loading_market_hours: bool = False
    market_hours_error: str = ""

    async def load_market_hours(self):
        self.is_loading_market_hours = True
        self.market_hours_error = ""
        try:
            service = MarketDataService()
            self.market_hours = await service.get_market_hours()
        except Exception as e:
            self.market_hours_error = str(e)
            import logging

            logging.exception(f"Error loading market hours: {e}")
        finally:
            self.is_loading_market_hours = False
