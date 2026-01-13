"""
Compliance Type Definitions

This module contains all TypedDict definitions for the Compliance module.
"""

from typing import TypedDict


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
