import reflex as rx
from app.services import PositionService
from app.states.positions.types import BondPositionItem


class BondPositionsMixin(rx.State, mixin=True):
    """
    Mixin providing Bond Positions data state.
    """

    bond_positions: list[BondPositionItem] = []
    is_loading_bond_positions: bool = False
    bond_positions_error: str = ""

    bond_positions_search: str = ""

    async def load_bond_positions_data(self):
        """Load bond positions data."""
        self.is_loading_bond_positions = True
        self.bond_positions_error = ""
        try:
            service = PositionService()
            self.bond_positions = await service.get_bond_positions()
        except Exception as e:
            self.bond_positions_error = str(e)
            import logging

            logging.exception(f"Error loading bond positions: {e}")
        finally:
            self.is_loading_bond_positions = False

    def set_bond_positions_search(self, query: str):
        self.bond_positions_search = query

    @rx.var(cache=True)
    def filtered_bond_positions(self) -> list[BondPositionItem]:
        data = self.bond_positions
        if self.bond_positions_search:
            query = self.bond_positions_search.lower()
            data = [
                item
                for item in data
                if query in item.get("ticker", "").lower()
                or query in item.get("issuer", "").lower()
            ]
        return data
