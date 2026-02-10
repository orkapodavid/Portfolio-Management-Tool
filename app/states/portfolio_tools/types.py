"""
Portfolio Tools Type Definitions

This module contains all TypedDict definitions for the Portfolio Tools module.
"""

from typing import TypedDict


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
    emsx_order: str
    emsx_remark: str
    emsx_working: str
    emsx_order_col: str
    emsx_filled: str


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