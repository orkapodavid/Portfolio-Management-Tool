"""
Market Data Type Definitions

This module contains all TypedDict definitions for the Market Data module.
"""

from typing import TypedDict


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
