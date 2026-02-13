"""
UI Type Definitions

TypedDicts for KPI metrics and top movers used by the performance header.
"""

from typing import TypedDict


class KPIMetric(TypedDict):
    label: str
    value: str
    is_positive: bool
    trend_data: str


class TopMover(TypedDict):
    ticker: str
    value: str
    change: str
    is_positive: bool
