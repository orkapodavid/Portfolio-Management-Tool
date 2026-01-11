import reflex as rx
from app.services import PositionService
from app.states.positions.types import StockPositionItem


class StockPositionMixin(rx.State, mixin=True):
    """
    Mixin providing Stock Position data state.
    """

    stock_positions: list[StockPositionItem] = []
    is_loading_stock_positions: bool = False
    stock_positions_error: str = ""

    stock_positions_search: str = ""

    async def load_stock_positions_data(self):
        """Load stock positions data."""
        self.is_loading_stock_positions = True
        self.stock_positions_error = ""
        try:
            service = PositionService()
            self.stock_positions = await service.get_stock_positions()
        except Exception as e:
            self.stock_positions_error = str(e)
            import logging

            logging.exception(f"Error loading stock positions: {e}")
        finally:
            self.is_loading_stock_positions = False

    def set_stock_positions_search(self, query: str):
        self.stock_positions_search = query

    @rx.var(cache=True)
    def filtered_stock_positions(self) -> list[StockPositionItem]:
        data = self.stock_positions
        if self.stock_positions_search:
            query = self.stock_positions_search.lower()
            data = [
                item
                for item in data
                if query in item.get("ticker", "").lower()
                or query in item.get("company_name", "").lower()
            ]
        return data
