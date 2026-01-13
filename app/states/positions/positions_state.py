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

    # Shared UI state for Positions tables
    sort_column: str = ""
    sort_direction: str = "asc"
    selected_row: int = -1

    def toggle_sort(self, column: str):
        """Toggle sort direction for a column."""
        if self.sort_column == column:
            self.sort_direction = "desc" if self.sort_direction == "asc" else "asc"
        else:
            self.sort_column = column
            self.sort_direction = "asc"

    def set_selected_row(self, row_id: int):
        """Set selected row ID."""
        self.selected_row = row_id

    def handle_generate(self, action: str):
        """Handle generate button actions."""
        print(f"Positions: Handle generate action: {action}")

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
