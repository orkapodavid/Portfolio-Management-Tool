"""
Instruments Type Definitions

This module contains all TypedDict definitions for the Instruments module.
"""

from typing import TypedDict


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
    dtl10: str
    ticker: str
    company: str
    country: str
    industry: str
    last_price: str
    mkt_cap_loc: str
    mkt_cap_usd: str
    adv_3m: str
    adv_3m_usd: str
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
