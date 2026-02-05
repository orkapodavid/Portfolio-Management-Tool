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

import asyncio
from datetime import datetime

import reflex as rx
from app.services import PortfolioToolsService
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

    # Loading states and timestamps for each grid
    is_loading_pay_to_hold: bool = False
    pay_to_hold_last_updated: str = "—"

    is_loading_short_ecl: bool = False
    short_ecl_last_updated: str = "—"

    is_loading_stock_borrow: bool = False
    stock_borrow_last_updated: str = "—"

    is_loading_po_settlement: bool = False
    po_settlement_last_updated: str = "—"

    is_loading_deal_indication: bool = False
    deal_indication_last_updated: str = "—"

    is_loading_reset_dates: bool = False
    reset_dates_last_updated: str = "—"

    is_loading_coming_resets: bool = False
    coming_resets_last_updated: str = "—"

    is_loading_cb_installments: bool = False
    cb_installments_last_updated: str = "—"

    is_loading_excess_amount: bool = False
    excess_amount_last_updated: str = "—"

    # UI state
    is_loading: bool = False
    current_tab: str = "pay_to_hold"

    # Shared UI state for sorting
    sort_column: str = ""
    sort_direction: str = "asc"
    selected_row: int = -1

    async def on_load(self):
        """Called when Portfolio Tools view loads."""
        await self.load_portfolio_tools_data()

    async def load_portfolio_tools_data(self):
        """Load all portfolio tools data from PortfolioToolsService."""
        self.is_loading = True
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            service = PortfolioToolsService()
            self.pay_to_hold = await service.get_pay_to_hold()
            self.pay_to_hold_last_updated = timestamp

            self.short_ecl = await service.get_short_ecl()
            self.short_ecl_last_updated = timestamp

            self.stock_borrow = await service.get_stock_borrow()
            self.stock_borrow_last_updated = timestamp

            self.po_settlement = await service.get_po_settlement()
            self.po_settlement_last_updated = timestamp

            self.deal_indication = await service.get_deal_indication()
            self.deal_indication_last_updated = timestamp

            self.reset_dates = await service.get_reset_dates()
            self.reset_dates_last_updated = timestamp

            self.coming_resets = await service.get_coming_resets()
            self.coming_resets_last_updated = timestamp

            self.cb_installments = await service.get_cb_installments()
            self.cb_installments_last_updated = timestamp

            self.excess_amount = await service.get_excess_amount()
            self.excess_amount_last_updated = timestamp
        except Exception as e:
            import logging

            logging.exception(f"Error loading portfolio tools data: {e}")
        finally:
            self.is_loading = False

    # =========================================================================
    # Force Refresh Methods
    # =========================================================================

    async def force_refresh_pay_to_hold(self):
        if self.is_loading_pay_to_hold:
            return
        self.is_loading_pay_to_hold = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = PortfolioToolsService()
            self.pay_to_hold = await service.get_pay_to_hold()
            self.pay_to_hold_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        finally:
            self.is_loading_pay_to_hold = False

    async def force_refresh_short_ecl(self):
        if self.is_loading_short_ecl:
            return
        self.is_loading_short_ecl = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = PortfolioToolsService()
            self.short_ecl = await service.get_short_ecl()
            self.short_ecl_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        finally:
            self.is_loading_short_ecl = False

    async def force_refresh_stock_borrow(self):
        if self.is_loading_stock_borrow:
            return
        self.is_loading_stock_borrow = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = PortfolioToolsService()
            self.stock_borrow = await service.get_stock_borrow()
            self.stock_borrow_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        finally:
            self.is_loading_stock_borrow = False

    async def force_refresh_po_settlement(self):
        if self.is_loading_po_settlement:
            return
        self.is_loading_po_settlement = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = PortfolioToolsService()
            self.po_settlement = await service.get_po_settlement()
            self.po_settlement_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        finally:
            self.is_loading_po_settlement = False

    async def force_refresh_deal_indication(self):
        if self.is_loading_deal_indication:
            return
        self.is_loading_deal_indication = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = PortfolioToolsService()
            self.deal_indication = await service.get_deal_indication()
            self.deal_indication_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        finally:
            self.is_loading_deal_indication = False

    async def force_refresh_reset_dates(self):
        if self.is_loading_reset_dates:
            return
        self.is_loading_reset_dates = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = PortfolioToolsService()
            self.reset_dates = await service.get_reset_dates()
            self.reset_dates_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        finally:
            self.is_loading_reset_dates = False

    async def force_refresh_coming_resets(self):
        if self.is_loading_coming_resets:
            return
        self.is_loading_coming_resets = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = PortfolioToolsService()
            self.coming_resets = await service.get_coming_resets()
            self.coming_resets_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        finally:
            self.is_loading_coming_resets = False

    async def force_refresh_cb_installments(self):
        if self.is_loading_cb_installments:
            return
        self.is_loading_cb_installments = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = PortfolioToolsService()
            self.cb_installments = await service.get_cb_installments()
            self.cb_installments_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        finally:
            self.is_loading_cb_installments = False

    async def force_refresh_excess_amount(self):
        if self.is_loading_excess_amount:
            return
        self.is_loading_excess_amount = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = PortfolioToolsService()
            self.excess_amount = await service.get_excess_amount()
            self.excess_amount_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        finally:
            self.is_loading_excess_amount = False

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
