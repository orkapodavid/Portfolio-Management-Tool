"""
UI Shared Type Definitions

This module contains shared TypedDict definitions used across UI components.
"""

from typing import TypedDict


class KPIMetric(TypedDict):
    label: str
    value: str
    is_positive: bool
    trend_data: str


class TopMover(TypedDict):
    ticker: str
    name: str
    value: str
    change: str
    is_positive: bool


class NotificationItem(TypedDict):
    id: int
    header: str
    ticker: str
    timestamp: str
    instruction: str
    type: str
    read: bool
