"""
Reconciliation Type Definitions

This module contains all TypedDict definitions for the Reconciliation module.
"""

from typing import TypedDict


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
