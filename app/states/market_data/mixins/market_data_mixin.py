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
