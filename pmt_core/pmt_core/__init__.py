"""
pmt_core - Shared Business Logic for Portfolio Management Tool

This package provides shared models, services, and utilities that can be used
by both the Reflex web application and future PyQt desktop integration.
"""

__version__ = "0.1.0"

from pmt_core.models import (
    # Types
    PositionRecord,
    PnLRecord,
    MarketDataRecord,
    OrderRecord,
    ComplianceRecord,
    RiskRecord,
    # Enums
    InstrumentType,
    DashboardSection,
    OrderStatus,
    ComplianceType,
)

__all__ = [
    "__version__",
    # Types
    "PositionRecord",
    "PnLRecord",
    "MarketDataRecord",
    "OrderRecord",
    "ComplianceRecord",
    "RiskRecord",
    # Enums
    "InstrumentType",
    "DashboardSection",
    "OrderStatus",
    "ComplianceType",
]
