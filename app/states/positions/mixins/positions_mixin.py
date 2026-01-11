import reflex as rx
from app.services import PositionService
from app.states.positions.types import PositionItem


class PositionsMixin(rx.State, mixin=True):
    """
    Mixin providing general Positions data state.
    """

    positions: list[PositionItem] = []
    is_loading_positions: bool = False
    positions_error: str = ""

    positions_search: str = ""

    async def load_positions_data(self):
        """Load positions data."""
        self.is_loading_positions = True
        self.positions_error = ""
        try:
            service = PositionService()
            self.positions = await service.get_positions()
        except Exception as e:
            self.positions_error = str(e)
            import logging

            logging.exception(f"Error loading positions: {e}")
        finally:
            self.is_loading_positions = False

    def set_positions_search(self, query: str):
        self.positions_search = query

    @rx.var(cache=True)
    def filtered_positions(self) -> list[PositionItem]:
        data = self.positions
        if self.positions_search:
            query = self.positions_search.lower()
            data = [
                item
                for item in data
                if query in item.get("ticker", "").lower()
                or query in item.get("description", "").lower()
            ]
        return data
