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

    def set_historical_data_search(self, query: str):
        self.historical_data_search = query

    @rx.var(cache=True)
    def filtered_historical_data(self) -> list[HistoricalDataItem]:
        data = self.historical_data
        if self.historical_data_search:
            query = self.historical_data_search.lower()
            data = [item for item in data if query in item.get("ticker", "").lower()]
        return data
