"""
PnL Type Definitions

This module contains all TypedDict definitions for the PnL module.
"""

from typing import TypedDict


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
