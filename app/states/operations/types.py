"""
Operations Type Definitions

This module contains all TypedDict definitions for the Operations module.
"""

from typing import TypedDict


class DailyProcedureItem(TypedDict):
    id: int
    check_date: str
    host_run_date: str
    scheduled_time: str
    procedure_name: str
    status: str
    error_message: str
    frequency: str
    scheduled_day: str
    created_by: str
    created_time: str


class OperationProcessItem(TypedDict):
    id: int
    process: str
    status: str
    last_run_time: str
