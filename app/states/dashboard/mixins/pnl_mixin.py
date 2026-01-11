"""
P&L Mixin - State functionality for Profit & Loss data

This Mixin provides all P&L-related state variables, computed vars,
and event handlers. It integrates with PnLService for data access.

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
Pattern: State Mixin for code reuse
"""

import reflex as rx
from app.services import PnLService
from app.states.dashboard.types import (
    PnLChangeItem,
    PnLSummaryItem,
    PnLCurrencyItem,
)


class PnLMixin(rx.State, mixin=True):
    """
    Mixin providing P&L data state and filtering.

    Data provided:
    - P&L changes (YTD, 1D, 1W, 1M)
    - P&L summary
    - Currency P&L
    """

    # P&L data lists
    pnl_change_list: list[PnLChangeItem] = []
    pnl_summary_list: list[PnLSummaryItem] = []
    pnl_currency_list: list[PnLCurrencyItem] = []

    async def load_pnl_data(self):
        """Load all P&L data from PnLService."""
        try:
            service = PnLService()
            self.pnl_change_list = await service.get_pnl_changes()
            self.pnl_summary_list = await service.get_pnl_summary()
            self.pnl_currency_list = await service.get_currency_pnl()
        except Exception as e:
            import logging

            logging.exception(f"Error loading P&L data: {e}")

    def _filter_pnl_by_ticker(self, items: list[dict], search_query: str) -> list[dict]:
        """Helper to filter P&L items by ticker or underlying."""
        if not search_query:
            return items
        query = search_query.lower()
        return [
            item
            for item in items
            if query in item.get("ticker", "").lower()
            or query in item.get("underlying", "").lower()
        ]
