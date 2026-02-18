import reflex as rx
from app.services import MarketDataService
from app.states.market_data.types import TickerDataItem
import logging

class TickerDataMixin(rx.State, mixin=True):
    """
    Mixin providing Ticker Data (Reference Data) state.
    """

    ticker_data: list[TickerDataItem] = []
    is_loading_ticker_data: bool = False
    ticker_data_error: str = ""

    ticker_data_search: str = ""

    async def load_ticker_data(self):
        self.is_loading_ticker_data = True
        self.ticker_data_error = ""
        try:
            service = MarketDataService()
            self.ticker_data = await service.get_ticker_data()
        except Exception as e:
            self.ticker_data_error = str(e)

            logging.exception(f"Error loading ticker data: {e}")
        finally:
            self.is_loading_ticker_data = False

    def set_ticker_data_search(self, query: str):
        self.ticker_data_search = query

    @rx.var(cache=True)
    def filtered_ticker_data(self) -> list[TickerDataItem]:
        data = self.ticker_data
        if self.ticker_data_search:
            query = self.ticker_data_search.lower()
            data = [
                item
                for item in data
                if query in item.get("ticker", "").lower()
                or query in item.get("description", "").lower()
            ]
        return data
