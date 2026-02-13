"""
Dashboard Type Definitions

TypedDict definitions for Dashboard module data structures.
"""

from typing import TypedDict


class UserItem(TypedDict):
    """User data item for the overview tab."""
    id: str
    name: str
    email: str
    role: str
    status: str
    last_login: str
    created_at: str


class ActivityItem(TypedDict):
    """Recent activity event."""
    type: str
    user: str
    detail: str
    time: str
    color: str


class MarketDataItem(TypedDict):
    """Market data row for the analytics AG Grid."""
    ticker: str
    company: str
    sector: str
    price: float
    change: float
    volume: int
    marketCap: str


class SummaryStats(TypedDict):
    """Summary statistics for market data."""
    total: int
    gainers: int
    losers: int
    avg_change: float
