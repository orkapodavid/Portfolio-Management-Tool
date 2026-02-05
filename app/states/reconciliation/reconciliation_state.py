"""
Reconciliation State - Module-specific state for Reconciliation data

Composes all Reconciliation mixins to provide unified interface.
Following the mixin-per-tab architecture pattern.
"""

import reflex as rx
from app.states.reconciliation.mixins.pps_recon_mixin import PPSReconMixin
from app.states.reconciliation.mixins.settlement_recon_mixin import SettlementReconMixin
from app.states.reconciliation.mixins.failed_trades_mixin import FailedTradesMixin
from app.states.reconciliation.mixins.pnl_recon_mixin import PnLReconMixin
from app.states.reconciliation.mixins.risk_input_recon_mixin import RiskInputReconMixin


class ReconciliationState(
    PPSReconMixin,
    SettlementReconMixin,
    FailedTradesMixin,
    PnLReconMixin,
    RiskInputReconMixin,
    rx.State,
):
    """
    Main Reconciliation module state.
    Inherits from all Reconciliation tab mixins to provide unified interface.
    """

    # Module-level state
    current_tab: str = "pps"  # "pps", "settlement", "failed", "pnl", "risk_input"

    # Shared UI state for sorting
    sort_column: str = ""
    sort_direction: str = "asc"
    selected_row: int = -1

    async def on_load(self):
        """Called when Reconciliation view loads."""
        await self.load_reconciliation_data()

    async def load_reconciliation_data(self):
        """Load all reconciliation data (backward compatible)."""
        await self.load_pps_recon_data()
        await self.load_settlement_recon_data()
        await self.load_failed_trades_data()
        await self.load_pnl_recon_data()
        await self.load_risk_input_recon_data()

    async def load_reconciliation_module_data(self):
        """Load data for the active tab only."""
        if self.current_tab == "pps":
            await self.load_pps_recon_data()
        elif self.current_tab == "settlement":
            await self.load_settlement_recon_data()
        elif self.current_tab == "failed":
            await self.load_failed_trades_data()
        elif self.current_tab == "pnl":
            await self.load_pnl_recon_data()
        elif self.current_tab == "risk_input":
            await self.load_risk_input_recon_data()

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
