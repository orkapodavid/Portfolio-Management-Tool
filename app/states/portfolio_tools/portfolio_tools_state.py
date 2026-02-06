"""
Portfolio Tools State - Module-specific state for Portfolio Tools data

Composes all portfolio tools-related tab mixins:
- Pay To Hold
- Short ECL
- Stock Borrow
- PO Settlement
- Deal Indication
- Reset Dates
- Coming Resets
- CB Installments
- Excess Amount
"""

import reflex as rx
from app.states.portfolio_tools.mixins import (
    PayToHoldMixin,
    ShortECLMixin,
    StockBorrowMixin,
    POSettlementMixin,
    DealIndicationMixin,
    ResetDatesMixin,
    ComingResetsMixin,
    CBInstallmentsMixin,
    ExcessAmountMixin,
)


class PortfolioToolsState(
    PayToHoldMixin,
    ShortECLMixin,
    StockBorrowMixin,
    POSettlementMixin,
    DealIndicationMixin,
    ResetDatesMixin,
    ComingResetsMixin,
    CBInstallmentsMixin,
    ExcessAmountMixin,
    rx.State,
):
    """
    State management for portfolio tools data.
    Composes all portfolio tools tab mixins for unified interface.
    """

    # UI state
    current_tab: str = "pay_to_hold"

    # Shared UI state for sorting
    sort_column: str = ""
    sort_direction: str = "asc"
    selected_row: int = -1

    async def on_load(self):
        """Called when Portfolio Tools view loads."""
        await self.load_portfolio_tools_data()

    async def load_portfolio_tools_data(self):
        """Load all portfolio tools data from mixins."""
        await self.load_pay_to_hold_data()
        await self.load_short_ecl_data()
        await self.load_stock_borrow_data()
        await self.load_po_settlement_data()
        await self.load_deal_indication_data()
        await self.load_reset_dates_data()
        await self.load_coming_resets_data()
        await self.load_cb_installments_data()
        await self.load_excess_amount_data()

    # =========================================================================
    # UI State Methods
    # =========================================================================

    def set_current_tab(self, tab: str):
        """Switch between portfolio tools tabs."""
        self.current_tab = tab

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
