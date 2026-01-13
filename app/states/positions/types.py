"""
Positions Type Definitions

This module contains all TypedDict definitions for the Positions module.
"""

from typing import TypedDict


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
