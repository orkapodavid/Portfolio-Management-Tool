"""
EMSX (Orders) Type Definitions

This module contains all TypedDict definitions for the EMSX/Orders module.
"""

from typing import TypedDict


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


class EMSXRouteItem(TypedDict):
    id: int
    sequence: str
    underlying: str
    ticker: str
    broker: str
    route_status: str
    route_amount: str
    route_filled: str
    route_avg_price: str
