"""
Portfolio Dashboard Type Definitions

This module contains all TypedDict definitions used across the portfolio dashboard
substates. Centralizing types here allows for code reuse and maintains consistency.

Refactoring Note:
This file was created as part of the portfolio_dashboard_state.py restructuring
to follow Reflex best practices for flat state architecture.

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
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
