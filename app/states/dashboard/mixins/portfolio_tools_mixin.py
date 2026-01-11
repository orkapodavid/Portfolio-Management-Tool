"""
Portfolio Tools Mixin - State functionality for Portfolio Tools data

This Mixin provides all portfolio tools-related state variables, computed vars,
and event handlers.

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
Pattern: State Mixin for code reuse
"""

import reflex as rx
from app.services import PortfolioService
from app.states.dashboard.types import (
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


class PortfolioToolsMixin(rx.State, mixin=True):
    """
    Mixin providing portfolio tools data state and filtering.

    Data provided:
    - Pay to hold
    - Short ECL
    - Stock borrow
    - PO settlement
    - Deal indication
    - Reset dates
    - Coming resets
    - CB installments
    - Excess amount
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

    async def load_portfolio_tools_data(self):
        """Load all portfolio tools data from PortfolioService."""
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
