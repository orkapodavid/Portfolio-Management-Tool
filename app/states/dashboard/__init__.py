"""
Portfolio Dashboard States Module

This module provides the unified PortfolioDashboardState class and all focused
Mixin classes for the portfolio dashboard.

Architecture:
- PortfolioDashboardState inherits from all Mixins (backward compatible)
- Each Mixin handles a specific domain (positions, P&L, risk, etc.)
- Components can import PortfolioDashboardState directly

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
"""

# Main unified state (backward compatible - most components should use this)
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState

# Individual mixins (for advanced use cases or direct access)
from app.states.dashboard.mixins import (
    PositionsMixin,
    PnLMixin,
    RiskMixin,
    ComplianceMixin,
    MarketDataMixin,
    ReconciliationMixin,
    OperationsMixin,
    PortfolioToolsMixin,
    InstrumentsMixin,
    EventsMixin,
    EMSXMixin,
    UIMixin,
)

# Legacy substates (kept for compatibility but may be deprecated)
from app.states.dashboard.positions_state import PositionsState
from app.states.dashboard.pnl_state import PnLState
from app.states.dashboard.risk_state import RiskState
from app.states.dashboard.market_data_state import MarketDataState
from app.states.dashboard.emsx_state import EMSXState
from app.states.dashboard.compliance_state import ComplianceState
from app.states.dashboard.reconciliation_state import ReconciliationState

__all__ = [
    # Main state (backward compatible)
    "PortfolioDashboardState",
    # Mixins
    "PositionsMixin",
    "PnLMixin",
    "RiskMixin",
    "ComplianceMixin",
    "MarketDataMixin",
    "ReconciliationMixin",
    "OperationsMixin",
    "PortfolioToolsMixin",
    "InstrumentsMixin",
    "EventsMixin",
    "EMSXMixin",
    "UIMixin",
    # Legacy substates
    "PositionsState",
    "PnLState",
    "RiskState",
    "MarketDataState",
    "EMSXState",
    "ComplianceState",
    "ReconciliationState",
]
