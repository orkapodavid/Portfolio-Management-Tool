"""
Events Type Definitions

This module contains all TypedDict definitions for the Events module.
"""

from typing import TypedDict


class EventCalendarItem(TypedDict):
    id: int
    underlying: str
    ticker: str
    company: str
    event_date: str
    day_of_week: str
    event_type: str
    time: str


class EventStreamItem(TypedDict):
    id: int
    symbol: str
    record_date: str
    event_date: str
    day_of_week: str
    event_type: str
    subject: str
    notes: str
    alerted: str
    recur: str
    created_by: str
    created_time: str
    updated_by: str
    updated_time: str


class ReverseInquiryItem(TypedDict):
    id: int
    ticker: str
    company: str
    inquiry_date: str
    expiry_date: str
    deal_point: str
    agent: str
    notes: str
