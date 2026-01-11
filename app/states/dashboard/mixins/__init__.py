"""
Dashboard State Mixins Package

This package contains Mixin classes that provide domain-specific state functionality.
Each Mixin uses `mixin=True` and provides data, events, and computed vars for a specific domain.

The Mixins are combined in PortfolioDashboardState to create a unified state class
while maintaining separation of concerns.

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
"""

from app.states.dashboard.mixins.positions_mixin import PositionsMixin
from app.states.dashboard.mixins.pnl_mixin import PnLMixin
from app.states.dashboard.mixins.risk_mixin import RiskMixin
from app.states.dashboard.mixins.compliance_mixin import ComplianceMixin
from app.states.dashboard.mixins.market_data_mixin import MarketDataMixin
from app.states.dashboard.mixins.reconciliation_mixin import ReconciliationMixin
from app.states.dashboard.mixins.operations_mixin import OperationsMixin
from app.states.dashboard.mixins.portfolio_tools_mixin import PortfolioToolsMixin
from app.states.dashboard.mixins.instruments_mixin import InstrumentsMixin
from app.states.dashboard.mixins.events_mixin import EventsMixin
from app.states.dashboard.mixins.emsx_mixin import EMSXMixin
from app.states.dashboard.mixins.ui_mixin import UIMixin

__all__ = [
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
]
