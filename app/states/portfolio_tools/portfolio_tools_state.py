"""
Portfolio Tools State - Module-specific state for Portfolio Tools data

Handles all portfolio tools-related data:
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
from app.services import PortfolioService
from app.states.portfolio_tools.types import (
    PayToHoldItem,
    ShortECLItem,
    StockBorrowItem,
    POSettlementItem,
    DealIndicationItem,
    ResetDateItem,
    ComingResetItem,
    CBInstallmentItem,
    ExcessAmountItem,
)


class PortfolioToolsState(rx.State):
    """
    State management for portfolio tools data.
    """

    # Portfolio tools data lists
    pay_to_hold: list[PayToHoldItem] = []
    short_ecl: list[ShortECLItem] = []
    stock_borrow: list[StockBorrowItem] = []
    po_settlement: list[POSettlementItem] = []
    deal_indication: list[DealIndicationItem] = []
    reset_dates: list[ResetDateItem] = []
    coming_resets: list[ComingResetItem] = []
    cb_installments: list[CBInstallmentItem] = []
    excess_amount: list[ExcessAmountItem] = []

    # UI state
    is_loading: bool = False
    current_search_query: str = ""
    current_tab: str = "pay_to_hold"

    # Shared UI state for sorting
    sort_column: str = ""
    sort_direction: str = "asc"
    selected_row: int = -1

    async def on_load(self):
        """Called when Portfolio Tools view loads."""
        await self.load_portfolio_tools_data()

    async def load_portfolio_tools_data(self):
        """Load all portfolio tools data from PortfolioService."""
        self.is_loading = True
        try:
            service = PortfolioService()
            self.pay_to_hold = await service.get_pay_to_hold()
            self.short_ecl = await service.get_short_ecl()
            self.stock_borrow = await service.get_stock_borrow()
            self.po_settlement = await service.get_po_settlement()
            self.deal_indication = await service.get_deal_indication()
            self.reset_dates = await service.get_reset_dates()
            self.coming_resets = await service.get_coming_resets()
            self.cb_installments = await service.get_cb_installments()
            self.excess_amount = await service.get_excess_amount()
        except Exception as e:
            import logging

            logging.exception(f"Error loading portfolio tools data: {e}")
        finally:
            self.is_loading = False

    def set_search_query(self, query: str):
        """Update search query for filtering."""
        self.current_search_query = query

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

    # Filtered Properties
    @rx.var(cache=True)
    def filtered_pay_to_hold(self) -> list[PayToHoldItem]:
        if not self.current_search_query:
            return self.pay_to_hold
        q = self.current_search_query.lower()
        return [i for i in self.pay_to_hold if q in str(i.values()).lower()]

    @rx.var(cache=True)
    def filtered_short_ecl(self) -> list[ShortECLItem]:
        if not self.current_search_query:
            return self.short_ecl
        q = self.current_search_query.lower()
        return [i for i in self.short_ecl if q in str(i.values()).lower()]

    @rx.var(cache=True)
    def filtered_stock_borrow(self) -> list[StockBorrowItem]:
        if not self.current_search_query:
            return self.stock_borrow
        q = self.current_search_query.lower()
        return [i for i in self.stock_borrow if q in str(i.values()).lower()]

    @rx.var(cache=True)
    def filtered_po_settlement(self) -> list[POSettlementItem]:
        if not self.current_search_query:
            return self.po_settlement
        q = self.current_search_query.lower()
        return [i for i in self.po_settlement if q in str(i.values()).lower()]

    @rx.var(cache=True)
    def filtered_deal_indication(self) -> list[DealIndicationItem]:
        if not self.current_search_query:
            return self.deal_indication
        q = self.current_search_query.lower()
        return [i for i in self.deal_indication if q in str(i.values()).lower()]

    @rx.var(cache=True)
    def filtered_reset_dates(self) -> list[ResetDateItem]:
        if not self.current_search_query:
            return self.reset_dates
        q = self.current_search_query.lower()
        return [i for i in self.reset_dates if q in str(i.values()).lower()]

    @rx.var(cache=True)
    def filtered_coming_resets(self) -> list[ComingResetItem]:
        if not self.current_search_query:
            return self.coming_resets
        q = self.current_search_query.lower()
        return [i for i in self.coming_resets if q in str(i.values()).lower()]

    @rx.var(cache=True)
    def filtered_cb_installments(self) -> list[CBInstallmentItem]:
        if not self.current_search_query:
            return self.cb_installments
        q = self.current_search_query.lower()
        return [i for i in self.cb_installments if q in str(i.values()).lower()]

    @rx.var(cache=True)
    def filtered_excess_amount(self) -> list[ExcessAmountItem]:
        if not self.current_search_query:
            return self.excess_amount
        q = self.current_search_query.lower()
        return [i for i in self.excess_amount if q in str(i.values()).lower()]
