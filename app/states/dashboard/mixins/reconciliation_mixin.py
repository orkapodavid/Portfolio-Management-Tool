"""
Reconciliation Mixin - State functionality for Reconciliation data

This Mixin provides all reconciliation-related state variables, computed vars,
and event handlers. It integrates with DatabaseService for data access.

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
Pattern: State Mixin for code reuse
"""

import reflex as rx
from app.services import DatabaseService
from app.states.dashboard.types import (
    PPSReconItem,
    SettlementReconItem,
    FailedTradeItem,
    PnLReconItem,
    RiskInputReconItem,
)


class ReconciliationMixin(rx.State, mixin=True):
    """
    Mixin providing reconciliation data state and filtering.

    Data provided:
    - PPS reconciliation
    - Settlement reconciliation
    - Failed trades
    - P&L reconciliation
    - Risk input reconciliation
    """

    # Reconciliation data lists
    pps_recon: list[PPSReconItem] = []
    settlement_recon: list[SettlementReconItem] = []
    failed_trades: list[FailedTradeItem] = []
    pnl_recon: list[PnLReconItem] = []
    risk_input_recon: list[RiskInputReconItem] = []

    async def load_reconciliation_data(self):
        """Load all reconciliation data from DatabaseService."""
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
