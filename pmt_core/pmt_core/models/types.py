"""
pmt_core.models.types - Preliminary TypedDict Definitions

These type definitions are based on the PMT documentation (docs/pmt.md) and
aligned with existing app/states/types.py definitions. They represent the
core data structures that will be shared between the Reflex web app and
PyQt desktop application.

Note: These are preliminary definitions. They will be refined once the
PyQt source code is available and exact field structures are confirmed.
"""

from typing import TypedDict, Optional


class PositionRecord(TypedDict):
    """
    Position data structure for holdings across all instrument types.

    Aligned with: PositionItem, StockPositionItem, WarrantPositionItem, BondPositionItem
    from app/states/types.py

    Source: position_full.report.ini, position_tab/*
    """

    id: int
    trade_date: str
    deal_num: str
    detail_id: str
    underlying: str
    ticker: str
    company_name: str
    sec_id: str
    sec_type: str  # 'stock', 'warrant', 'bond', 'convertible'
    subtype: Optional[str]
    currency: str
    account_id: str
    pos_loc: str  # Position location
    notional: Optional[str]
    position: Optional[str]  # Quantity
    market_value: Optional[str]


class PnLRecord(TypedDict):
    """
    Profit and Loss data structure.

    Aligned with: PnLFullItem, PnLSummaryItem, PnLChangeItem
    from app/states/types.py

    Source: pnl_tab/*.report.ini
    """

    id: int
    trade_date: str
    underlying: str
    ticker: str
    currency: str
    # P&L values
    pnl_ytd: str
    pnl_mtd: Optional[str]
    pnl_wtd: Optional[str]
    pnl_dtd: Optional[str]
    # P&L changes
    pnl_chg_1d: str
    pnl_chg_1w: str
    pnl_chg_1m: str
    # P&L change percentages
    pnl_chg_pct_1d: str
    pnl_chg_pct_1w: str
    pnl_chg_pct_1m: str
    # Market data
    price: Optional[str]
    price_t_1: Optional[str]
    price_change: Optional[str]
    fx_rate: Optional[str]


class MarketDataRecord(TypedDict):
    """
    Market data structure for real-time and historical data.

    Aligned with: MarketDataItem, FXDataItem, HistoricalDataItem
    from app/states/types.py

    Source: market_data_tab/market_data.report.ini
    Data: Bloomberg real-time via worker_market_data.py
    """

    id: int
    ticker: str
    currency: Optional[str]
    # Pricing
    last_price: str
    bid: str
    ask: str
    vwap_price: Optional[str]
    # Volume
    last_volume: str
    listed_shares: Optional[str]
    # Changes
    chg_1d_pct: str
    implied_vol_pct: Optional[str]
    # Status
    market_status: str
    # Audit
    created_by: Optional[str]
    created_time: Optional[str]
    updated_by: Optional[str]
    updated_time: Optional[str]


class OrderRecord(TypedDict):
    """
    Order data structure for EMSX trading orders.

    Aligned with: EMSAOrderItem from app/states/types.py

    Source: trading_tab/emsx_order.report.ini, emsx_order_class.py
    Data: Live EMSX via EMSXOrderWorker + DB fallback
    """

    id: int
    sequence: str
    underlying: str
    ticker: str
    broker: str
    pos_loc: str
    side: str  # 'buy', 'sell'
    status: str  # 'working', 'filled', 'cancelled', etc.
    # Amounts
    order_amount: str
    routed_amount: str
    working_amount: str
    filled_amount: str
    # Pricing
    limit_price: Optional[str]
    avg_fill_price: Optional[str]
    # Timing
    order_time: Optional[str]
    last_update_time: Optional[str]


class ComplianceRecord(TypedDict):
    """
    Compliance data structure for restricted lists and undertakings.

    Aligned with: RestrictedListItem, UndertakingItem, BeneficialOwnershipItem
    from app/states/types.py

    Source: compliance_tab/*.report.ini
    """

    id: int
    ticker: str
    company_name: str
    # Compliance status
    compliance_type: str  # 'restricted', 'undertaking', 'beneficial_ownership'
    in_emsx: Optional[str]
    firm_block: Optional[str]
    # Dates
    compliance_start: Optional[str]
    nda_end: Optional[str]
    mnpi_end: Optional[str]
    wc_end: Optional[str]
    undertaking_expiry: Optional[str]
    # Details
    account: Optional[str]
    undertaking_type: Optional[str]
    undertaking_details: Optional[str]


class RiskRecord(TypedDict):
    """
    Risk data structure for Greeks and risk measures.

    Aligned with: RiskMeasureItem, RiskInputItem, DeltaChangeItem
    from app/states/types.py

    Source: analytics_tab/*.report.ini
    """

    id: int
    underlying: str
    ticker: str
    company_name: Optional[str]
    sec_type: str
    currency: str
    fx_rate: str
    # Risk inputs
    spot_price: str
    valuation_price: Optional[str]
    # Greeks
    delta: Optional[str]
    gamma: Optional[str]
    vega: Optional[str]
    theta: Optional[str]
    # Position Greeks
    pos_delta: Optional[str]
    pos_gamma: Optional[str]
    # Simulation parameters
    seed: Optional[str]
    simulation_num: Optional[str]
    trial_num: Optional[str]
    # Notional
    notional: Optional[str]
    notional_used: Optional[str]
    notional_current: Optional[str]
    is_private: Optional[str]
