import reflex as rx
from app.services import PositionService
from app.states.positions.types import WarrantPositionItem


class WarrantPositionMixin(rx.State, mixin=True):
    """
    Mixin providing Warrant Position data state.
    """

    warrant_positions: list[WarrantPositionItem] = []
    is_loading_warrant_positions: bool = False
    warrant_positions_error: str = ""

    warrant_positions_search: str = ""

    async def load_warrant_positions_data(self):
        """Load warrant positions data."""
        self.is_loading_warrant_positions = True
        self.warrant_positions_error = ""
        try:
            service = PositionService()
            self.warrant_positions = await service.get_warrant_positions()
        except Exception as e:
            self.warrant_positions_error = str(e)
            import logging

            logging.exception(f"Error loading warrant positions: {e}")
        finally:
            self.is_loading_warrant_positions = False

    def set_warrant_positions_search(self, query: str):
        self.warrant_positions_search = query

    @rx.var(cache=True)
    def filtered_warrant_positions(self) -> list[WarrantPositionItem]:
        data = self.warrant_positions
        if self.warrant_positions_search:
            query = self.warrant_positions_search.lower()
            data = [
                item
                for item in data
                if query in item.get("ticker", "").lower()
                or query in item.get("underlying", "").lower()
            ]
        return data
