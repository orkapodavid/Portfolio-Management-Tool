"""
Reconciliation State - Module-specific state for Reconciliation data

Handles all reconciliation-related data:
- PPS Reconciliation
- Settlement Reconciliation
- Failed Trades
- PnL Reconciliation
- Risk Input Reconciliation
"""

import reflex as rx
from app.services import DatabaseService
from app.states.reconciliation.types import (
    PPSReconItem,
    SettlementReconItem,
    FailedTradeItem,
    PnLReconItem,
    RiskInputReconItem,
)


class ReconciliationState(rx.State):
    """
    State management for reconciliation data.
    """

    # Reconciliation data lists
    pps_recon: list[PPSReconItem] = []
    settlement_recon: list[SettlementReconItem] = []
    failed_trades: list[FailedTradeItem] = []
    pnl_recon: list[PnLReconItem] = []
    risk_input_recon: list[RiskInputReconItem] = []

    # UI state
    is_loading: bool = False
    current_search_query: str = ""
    current_tab: str = "pps"

    # Shared UI state for sorting
    sort_column: str = ""
    sort_direction: str = "asc"
    selected_row: int = -1

    async def on_load(self):
        """Called when Reconciliation view loads."""
        await self.load_reconciliation_data()

    async def load_reconciliation_data(self):
        """Load all reconciliation data from DatabaseService."""
        self.is_loading = True
        try:
            service = DatabaseService()
            self.pps_recon = await service.get_pps_recon()
            self.settlement_recon = await service.get_settlement_recon()
            self.failed_trades = await service.get_failed_trades()
            self.pnl_recon = await service.get_pnl_recon()
            self.risk_input_recon = await service.get_risk_input_recon()
        except Exception as e:
            import logging

            logging.exception(f"Error loading reconciliation data: {e}")
        finally:
            self.is_loading = False

    def set_search_query(self, query: str):
        """Update search query for filtering."""
        self.current_search_query = query

    def set_current_tab(self, tab: str):
        """Switch between reconciliation tabs."""
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

    @rx.var(cache=True)
    def filtered_pps_recon(self) -> list[PPSReconItem]:
        """Filtered PPS reconciliation based on search query."""
        if not self.current_search_query:
            return self.pps_recon

        query = self.current_search_query.lower()
        return [
            item
            for item in self.pps_recon
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_settlement_recon(self) -> list[SettlementReconItem]:
        """Filtered settlement reconciliation based on search query."""
        if not self.current_search_query:
            return self.settlement_recon

        query = self.current_search_query.lower()
        return [
            item
            for item in self.settlement_recon
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_failed_trades(self) -> list[FailedTradeItem]:
        """Filtered failed trades based on search query."""
        if not self.current_search_query:
            return self.failed_trades

        query = self.current_search_query.lower()
        return [
            item
            for item in self.failed_trades
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
            or query in item.get("broker", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_pnl_recon(self) -> list[PnLReconItem]:
        """Filtered PnL reconciliation based on search query."""
        if not self.current_search_query:
            return self.pnl_recon

        query = self.current_search_query.lower()
        return [
            item
            for item in self.pnl_recon
            if query in item.get("underlying", "").lower()
            or query in item.get("deal_num", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_risk_input_recon(self) -> list[RiskInputReconItem]:
        """Filtered risk input reconciliation based on search query."""
        if not self.current_search_query:
            return self.risk_input_recon

        query = self.current_search_query.lower()
        return [
            item
            for item in self.risk_input_recon
            if query in item.get("ticker", "").lower()
            or query in item.get("underlying", "").lower()
        ]
