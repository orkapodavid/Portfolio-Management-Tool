"""
Portfolio Dashboard States Module

This module provides focused, independent state classes for the portfolio dashboard,
following Reflex best practices for flat state architecture.

Each substate:
- Handles a single responsibility (positions, P&L, risk, etc.)
- Integrates with appropriate service classes
- Loads data only when needed (via on_load())
- Is independent and doesn't create deep inheritance hierarchies

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc

Substates:
- PositionsState: Stock, warrant, and bond positions
- PnLState: Profit & loss data and calculations
- RiskState: Delta changes, risk measures, and risk inputs
- MarketDataState: Real-time market data and FX rates
- EMSXState: Bloomberg EMSX orders and routes
- ComplianceState: Restricted lists, undertakings, beneficial ownership
- ReconciliationState: PPS recon, settlement recon, failed trades

Type Definitions:
- types.py: Centralized TypedDict definitions for all substates
"""

from app.states.dashboard.positions_state import PositionsState
from app.states.dashboard.pnl_state import PnLState
from app.states.dashboard.risk_state import RiskState
from app.states.dashboard.market_data_state import MarketDataState
from app.states.dashboard.emsx_state import EMSXState
from app.states.dashboard.compliance_state import ComplianceState
from app.states.dashboard.reconciliation_state import ReconciliationState

# Keep original dashboard_state for backward compatibility if needed
# from app.states.dashboard.dashboard_state import DashboardState

__all__ = [
    "PositionsState",
    "PnLState",
    "RiskState",
    "MarketDataState",
    "EMSXState",
    "ComplianceState",
    "ReconciliationState",
    # "DashboardState",  # Legacy - use focused substates instead
]
