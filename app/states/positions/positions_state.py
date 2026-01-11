import reflex as rx
from app.states.positions.mixins.positions_mixin import PositionsMixin
from app.states.positions.mixins.stock_position_mixin import StockPositionMixin
from app.states.positions.mixins.warrant_position_mixin import WarrantPositionMixin
from app.states.positions.mixins.bond_positions_mixin import BondPositionsMixin
from app.states.positions.mixins.trade_summary_mixin import TradeSummaryMixin


class PositionsState(
    PositionsMixin,
    StockPositionMixin,
    WarrantPositionMixin,
    BondPositionsMixin,
    TradeSummaryMixin,
    rx.State,
):
    """
    Main Positions module state.
    Inherits from all Positions subtab mixins.
    """

    active_positions_subtab: str = "Positions"

    async def load_positions_module_data(self):
        """Load data for the active subtab."""
        if self.active_positions_subtab == "Positions":
            await self.load_positions_data()
        elif self.active_positions_subtab == "Stock Position":
            await self.load_stock_positions_data()
        elif self.active_positions_subtab == "Warrant Position":
            await self.load_warrant_positions_data()
        elif self.active_positions_subtab == "Bond Positions":
            await self.load_bond_positions_data()
        elif self.active_positions_subtab == "Trade Summary":
            await self.load_trade_summary_data()

    def set_positions_subtab(self, subtab: str):
        self.active_positions_subtab = subtab
