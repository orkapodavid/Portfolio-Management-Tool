import reflex as rx
from app.services import MarketDataService
from app.states.market_data.types import FXDataItem


class FXDataMixin(rx.State, mixin=True):
    """
    Mixin providing FX Data state.
    """

    fx_data: list[FXDataItem] = []
    is_loading_fx_data: bool = False
    fx_data_error: str = ""

    fx_data_search: str = ""

    async def load_fx_data(self):
        self.is_loading_fx_data = True
        self.fx_data_error = ""
        try:
            service = MarketDataService()
            self.fx_data = await service.get_fx_data()
        except Exception as e:
            self.fx_data_error = str(e)
            import logging

            logging.exception(f"Error loading FX data: {e}")
        finally:
            self.is_loading_fx_data = False

    def set_fx_data_search(self, query: str):
        self.fx_data_search = query

    @rx.var(cache=True)
    def filtered_fx_data(self) -> list[FXDataItem]:
        data = self.fx_data
        if self.fx_data_search:
            query = self.fx_data_search.lower()
            data = [item for item in data if query in item.get("pair", "").lower()]
        return data
