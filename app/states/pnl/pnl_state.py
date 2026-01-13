import reflex as rx
from app.states.pnl.mixins.pnl_change_mixin import PnLChangeMixin
from app.states.pnl.mixins.pnl_summary_mixin import PnLSummaryMixin
from app.states.pnl.mixins.pnl_currency_mixin import PnLCurrencyMixin
from app.states.pnl.mixins.pnl_full_mixin import PnLFullMixin


class PnLState(
    PnLChangeMixin,
    PnLSummaryMixin,
    PnLCurrencyMixin,
    PnLFullMixin,
    rx.State,
):
    """
    Main PnL module state.
    Inherits from all PnL subtab mixins to provide unified interface.
    """

    # Module-level state
    active_pnl_subtab: str = "PnL Change"

    # Shared UI state for PnL tables
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

    async def load_pnl_module_data(self):
        """Load data for the active subtab."""
        if self.active_pnl_subtab == "PnL Change":
            await self.load_pnl_change_data()
        elif self.active_pnl_subtab == "PnL Summary":
            await self.load_pnl_summary_data()
        elif self.active_pnl_subtab == "PnL Currency":
            await self.load_pnl_currency_data()
        elif self.active_pnl_subtab == "PnL Full":
            await self.load_pnl_full_data()

    def set_pnl_subtab(self, subtab: str):
        self.active_pnl_subtab = subtab
