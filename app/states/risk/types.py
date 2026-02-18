"""
Risk Type Definitions

This module contains all TypedDict definitions for the Risk module.
"""

from typing import TypedDict


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
    pos_gamma: str


class RiskMeasureItem(TypedDict):
    id: int
    seed: str
    simulation_num: str
    trial_num: str
    underlying: str
    ticker: str
    sec_type: str
    is_private: str
    notional: str
    notional_used: str
    notional_current: str
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
    notional: str
    notional_used: str
    notional_current: str
    currency: str
    fx_rate: str
    spot_price: str
