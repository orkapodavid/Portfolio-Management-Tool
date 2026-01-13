"""
Shared Type Definitions

This module contains TypedDict definitions used across the application states.
Centralizing types here allows for code reuse and maintains consistency.
"""

from typing import TypedDict


# Position Types
class PositionItem(TypedDict):
    id: int
    trade_date: str
    deal_num: str
    detail_id: str
    underlying: str
    ticker: str
    company_name: str
    account_id: str
    pos_loc: str


class StockPositionItem(TypedDict):
    id: int
    trade_date: str
    deal_num: str
    detail_id: str
    ticker: str
    company_name: str
    sec_id: str
    sec_type: str
    currency: str
    account_id: str
    position_location: str
    notional: str


class WarrantPositionItem(TypedDict):
    id: int
    trade_date: str
    deal_num: str
    detail_id: str
    underlying: str
    ticker: str
    company_name: str
    sec_id: str
    sec_type: str
    subtype: str
    currency: str
    account_id: str


class BondPositionItem(TypedDict):
    id: int
    trade_date: str
    deal_num: str
    detail_id: str
    underlying: str
    ticker: str
    company_name: str
    sec_id: str
    sec_type: str
    subtype: str
    currency: str
    account_id: str

    # P&L Types


class PnLChangeItem(TypedDict):
    id: int
    trade_date: str
    underlying: str
    ticker: str
    pnl_ytd: str
    pnl_chg_1d: str
    pnl_chg_1w: str
    pnl_chg_1m: str
    pnl_chg_pct_1d: str
    pnl_chg_pct_1w: str
    pnl_chg_pct_1m: str


class PnLFullItem(TypedDict):
    id: int
    trade_date: str
    underlying: str
    ticker: str
    pnl_ytd: str
    pnl_chg_1d: str
    pnl_chg_1w: str
    pnl_chg_1m: str
    pnl_chg_pct_1d: str
    pnl_chg_pct_1w: str
    pnl_chg_pct_1m: str


class PnLSummaryItem(TypedDict):
    id: int
    trade_date: str
    underlying: str
    currency: str
    price: str
    price_t_1: str
    price_change: str
    fx_rate: str
    fx_rate_t_1: str
    fx_rate_change: str
    dtl: str
    last_volume: str
    adv_3m: str


class PnLCurrencyItem(TypedDict):
    id: int
    trade_date: str
    currency: str
    fx_rate: str
    fx_rate_t_1: str
    fx_rate_change: str
    ccy_exposure: str
    usd_exposure: str
    pos_ccy_expo: str
    ccy_hedged_pnl: str
    pos_ccy_pnl: str
    net_ccy: str
    pos_c_truncated: str


# Risk Types
class DeltaChangeItem(TypedDict):
    id: int
    ticker: str
    company_name: str
    structure: str
    currency: str
    fx_rate: str
    current_price: str
    valuation_price: str
    pos_delta: str
    pos_delta_small: str
    pos_g: str


class RiskMeasureItem(TypedDict):
    id: int
    seed: str
    simulation_num: str
    trial_num: str
    underlying: str
    ticker: str
    sec_type: str
    is_private: str
    national: str
    national_used: str
    national_current: str
    currency: str
    fx_rate: str
    spot_price: str


class RiskInputItem(TypedDict):
    id: int
    seed: str
    simulation_num: str
    trial_num: str
    underlying: str
    ticker: str
    sec_type: str
    is_private: str
    national: str
    national_used: str
    national_current: str
    currency: str
    fx_rate: str
    spot_price: str


# EMSX Types
class EMSAOrderItem(TypedDict):
    id: int
    sequence: str
    underlying: str
    ticker: str
    broker: str
    pos_loc: str
    side: str
    status: str
    emsa_amount: str
    emsa_routed: str
    emsa_working: str
    emsa_filled: str


# Compliance Types
class RestrictedListItem(TypedDict):
    id: int
    ticker: str
    company_name: str
    in_emdx: str
    compliance_type: str
    firm_block: str
    compliance_start: str
    nda_end: str
    mnpi_end: str
    wc_end: str


class UndertakingItem(TypedDict):
    id: int
    deal_num: str
    ticker: str
    company_name: str
    account: str
    undertaking_expiry: str
    undertaking_type: str
    undertaking_details: str


class BeneficialOwnershipItem(TypedDict):
    id: int
    trade_date: str
    ticker: str
    company_name: str
    nosh_reported: str
    nosh_bbg: str
    nosh_proforma: str
    stock_shares: str
    warrant_shares: str
    bond_shares: str
    total_shares: str


# UI Types
class KPIMetric(TypedDict):
    label: str
    value: str
    is_positive: bool
    trend_data: str


class TopMover(TypedDict):
    ticker: str
    name: str
    value: str
    change: str
    is_positive: bool


class NotificationItem(TypedDict):
    id: int
    header: str
    ticker: str
    timestamp: str
    instruction: str
    type: str
    read: bool


# Trade Types
class TradeSummaryItem(TypedDict):
    id: int
    deal_num: str
    detail_id: str
    ticker: str
    underlying: str
    account_id: str
    company_name: str
    sec_id: str
    sec_type: str
    subtype: str
    currency: str
    closing_date: str
    divisor: str


# Compliance Additional Types
class MonthlyExerciseLimitItem(TypedDict):
    id: int
    underlying: str
    ticker: str
    company_name: str
    sec_type: str
    original_nosh: str
    original_quantity: str
    monthly_exercised_quantity: str
    monthly_exercised_pct: str
    monthly_sal: str


# Portfolio Tools Types
class PayToHoldItem(TypedDict):
    id: int
    trade_date: str
    ticker: str
    currency: str
    counter_party: str
    side: str
    sl_rate: str
    pth_amount_sod: str
    pth_amount: str
    emsa_order: str
    emsa_remark: str
    emsa_working: str
    emsa_order_col: str
    emsa_filled: str


class ShortECLItem(TypedDict):
    id: int
    trade_date: str
    ticker: str
    company_name: str
    pos_loc: str
    account: str
    short_position: str
    nosh: str
    short_ownership: str
    last_volume: str
    short_pos_truncated: str


class StockBorrowItem(TypedDict):
    id: int
    trade_date: str
    ticker: str
    company_name: str
    jpm_req: str
    jpm_firm: str
    borrow_rate: str
    bofa_req: str
    bofa_firm: str


class POSettlementItem(TypedDict):
    id: int
    deal_num: str
    ticker: str
    company_name: str
    structure: str
    currency: str
    fx_rate: str
    last_price: str
    current_position: str
    shares_allocated: str
    shares_swap: str
    shares_hedged: str


class DealIndicationItem(TypedDict):
    id: int
    ticker: str
    company_name: str
    identification: str
    deal_type: str
    agent: str
    captain: str
    indication_date: str
    currency: str
    market_cap_loc: str
    gross_proceed_loc: str
    indication_amount: str


class ResetDateItem(TypedDict):
    id: int
    underlying: str
    ticker: str
    company_name: str
    sec_type: str
    currency: str
    trade_date: str
    first_reset: str
    expiry: str
    latest_reset: str
    reset_up_down: str
    market_price: str


class ComingResetItem(TypedDict):
    id: int
    deal_num: str
    detail_id: str
    ticker: str
    account: str
    company_name: str
    announce_date: str
    closing_date: str
    cal_days: str
    biz_days: str


class CBInstallmentItem(TypedDict):
    id: int
    underlying: str
    ticker: str
    currency: str
    installment_date: str
    total_amount: str
    outstanding: str
    redeemed: str
    deferred: str
    converted: str
    installment_amount: str
    period: str


class ExcessAmountItem(TypedDict):
    id: int
    deal_num: str
    underlying: str
    ticker: str
    company_name: str
    warrants: str
    excess_amount: str
    threshold: str
    cb_redeem: str
    redeem: str


# Reconciliation Types
class PPSReconItem(TypedDict):
    id: int
    value_date: str
    trade_date: str
    underlying: str
    ticker: str
    code: str
    company_name: str
    sec_type: str
    pos_loc: str
    account: str


class SettlementReconItem(TypedDict):
    id: int
    trade_date: str
    ml_report_date: str
    underlying: str
    ticker: str
    company_name: str
    pos_loc: str
    currency: str
    sec_type: str
    position_settled: str
    ml_inventory: str


class FailedTradeItem(TypedDict):
    id: int
    report_date: str
    trade_date: str
    value_date: str
    settlement_date: str
    portfolio_code: str
    instrument_ref: str
    instrument_name: str
    ticker: str
    company_name: str
    isin: str
    sedol: str
    broker: str
    glass_reference: str
    trade_reference: str
    deal_type: str
    q: str


class PnLReconItem(TypedDict):
    id: int
    trade_date: str
    report_date: str
    deal_num: str
    row_index: str
    underlying: str
    pos_loc: str
    stock_sec_id: str
    warrant_sec_id: str
    bond_sec_id: str
    stock_position: str


class RiskInputReconItem(TypedDict):
    id: int
    value_date: str
    underlying: str
    ticker: str
    sec_type: str
    spot_mc: str
    spot_ppd: str
    position: str
    value_mc: str
    value_ppd: str


# Operations Types
class DailyProcedureItem(TypedDict):
    id: int
    check_date: str
    host_run_date: str
    scheduled_time: str
    procedure_name: str
    status: str
    error_message: str
    frequency: str
    scheduled_day: str
    created_by: str
    created_time: str


class OperationProcessItem(TypedDict):
    id: int
    process: str
    status: str
    last_run_time: str


# Market Data Types
class MarketDataItem(TypedDict):
    id: int
    ticker: str
    listed_shares: str
    last_volume: str
    last_price: str
    vwap_price: str
    bid: str
    ask: str
    chg_1d_pct: str
    implied_vol_pct: str
    market_status: str
    created_by: str


class FXDataItem(TypedDict):
    id: int
    ticker: str
    last_price: str
    bid: str
    ask: str
    created_by: str
    created_time: str
    updated_by: str
    update: str


class HistoricalDataItem(TypedDict):
    id: int
    trade_date: str
    ticker: str
    vwap_price: str
    last_price: str
    last_volume: str
    chg_1d_pct: str
    created_by: str
    created_time: str
    updated_by: str
    update: str


class TradingCalendarItem(TypedDict):
    id: int
    trade_date: str
    day_of_week: str
    usa: str
    hkg: str
    jpn: str
    aus: str
    nzl: str
    kor: str
    chn: str
    twn: str
    ind: str


class MarketHoursItem(TypedDict):
    id: int
    market: str
    ticker: str
    session: str
    local_time: str
    session_period: str
    is_open: str
    timezone: str


# Events Types
class EventCalendarItem(TypedDict):
    id: int
    underlying: str
    ticker: str
    company: str
    event_date: str
    day_of_week: str
    event_type: str
    time: str


class EventStreamItem(TypedDict):
    id: int
    symbol: str
    record_date: str
    event_date: str
    day_of_week: str
    event_type: str
    subject: str
    notes: str
    alerted: str
    recur: str
    created_by: str
    created_time: str
    updated_by: str
    updated_time: str


class ReverseInquiryItem(TypedDict):
    id: int
    ticker: str
    company: str
    inquiry_date: str
    expiry_date: str
    deal_point: str
    agent: str
    notes: str


# Instruments Types
class TickerDataItem(TypedDict):
    id: int
    ticker: str
    currency: str
    fx_rate: str
    sector: str
    company: str
    po_lead_manager: str
    fmat_cap: str
    smkt_cap: str
    chg_1d_pct: str
    dtl: str


class StockScreenerItem(TypedDict):
    id: int
    otl: str
    mkt_cap_37_pct: str
    ticker: str
    company: str
    country: str
    industry: str
    last_price: str
    mkt_cap_loc: str
    mkt_cap_usd: str
    adv_3m: str
    locate_qty_mm: str
    locate_f: str


class SpecialTermItem(TypedDict):
    id: int
    deal_num: str
    ticker: str
    company_name: str
    sec_type: str
    pos_loc: str
    account: str
    effective_date: str
    position: str


class InstrumentDataItem(TypedDict):
    id: int
    deal_num: str
    detail_id: str
    underlying: str
    ticker: str
    company_name: str
    sec_id: str
    sec_type: str
    pos_loc: str
    account: str


class InstrumentTermItem(TypedDict):
    id: int
    deal_num: str
    detail_id: str
    underlying: str
    ticker: str
    company_name: str
    sec_type: str
    effective_date: str
    maturity_date: str
    first_reset_da: str


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
