"""
Shared Type Definitions — re-exports from per-module types.

IMPORTANT: All TypedDicts are now defined in their per-module types.py files.
This file re-exports them for backward compatibility so that existing imports
like `from app.states.types import PnLChangeItem` continue to work.

Only `Holding` and `GenericTableItem` are defined here as they are cross-cutting
types with no single owning module.
"""

from typing import TypedDict

# ---------------------------------------------------------------------------
# PnL Types
# ---------------------------------------------------------------------------
from app.states.pnl.types import (  # noqa: F401
    PnLChangeItem,
    PnLFullItem,
    PnLSummaryItem,
    PnLCurrencyItem,
)

# ---------------------------------------------------------------------------
# Risk Types
# ---------------------------------------------------------------------------
from app.states.risk.types import (  # noqa: F401
    DeltaChangeItem,
    RiskMeasureItem,
    RiskInputItem,
)

# ---------------------------------------------------------------------------
# Position Types
# ---------------------------------------------------------------------------
from app.states.positions.types import (  # noqa: F401
    PositionItem,
    StockPositionItem,
    WarrantPositionItem,
    BondPositionItem,
    TradeSummaryItem,
)

# ---------------------------------------------------------------------------
# Market Data Types
# ---------------------------------------------------------------------------
from app.states.market_data.types import (  # noqa: F401
    MarketDataItem,
    FXDataItem,
    HistoricalDataItem,
    TradingCalendarItem,
    MarketHoursItem,
)
# TickerDataItem is defined in both market_data and instruments — canonical
# source is instruments/types.py (used by stock screener + ticker data grids).

# ---------------------------------------------------------------------------
# EMSX Types
# ---------------------------------------------------------------------------
from app.states.emsx.types import (  # noqa: F401
    EMSXOrderItem,
    EMSXRouteItem,
)

# ---------------------------------------------------------------------------
# Compliance Types
# ---------------------------------------------------------------------------
from app.states.compliance.types import (  # noqa: F401
    RestrictedListItem,
    UndertakingItem,
    BeneficialOwnershipItem,
    MonthlyExerciseLimitItem,
)

# ---------------------------------------------------------------------------
# Portfolio Tools Types
# ---------------------------------------------------------------------------
from app.states.portfolio_tools.types import (  # noqa: F401
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

# ---------------------------------------------------------------------------
# Reconciliation Types
# ---------------------------------------------------------------------------
from app.states.reconciliation.types import (  # noqa: F401
    PPSReconItem,
    SettlementReconItem,
    FailedTradeItem,
    PnLReconItem,
    RiskInputReconItem,
)

# ---------------------------------------------------------------------------
# Operations Types
# ---------------------------------------------------------------------------
from app.states.operations.types import (  # noqa: F401
    DailyProcedureItem,
    OperationProcessItem,
)

# ---------------------------------------------------------------------------
# Events Types
# ---------------------------------------------------------------------------
from app.states.events.types import (  # noqa: F401
    EventCalendarItem,
    EventStreamItem,
    ReverseInquiryItem,
)

# ---------------------------------------------------------------------------
# Instruments Types
# ---------------------------------------------------------------------------
from app.states.instruments.types import (  # noqa: F401
    TickerDataItem,
    StockScreenerItem,
    SpecialTermItem,
    InstrumentDataItem,
    InstrumentTermItem,
)

# ---------------------------------------------------------------------------
# UI Types
# ---------------------------------------------------------------------------
from app.states.ui.types import (  # noqa: F401
    KPIMetric,
    TopMover,
)

# ---------------------------------------------------------------------------
# Cross-cutting types (no owning module)
# ---------------------------------------------------------------------------


class Holding(TypedDict):
    symbol: str
    name: str
    shares: float
    avg_cost: float
    current_price: float
    daily_change_pct: float
    asset_class: str


class GenericTableItem(TypedDict):
    id: int
    ticker: str
    description: str
    asset_class: str
    qty: str
    price: str
    mkt_value: str
    daily_pnl: str
    status: str
    is_reconciled: bool
    is_positive: bool
