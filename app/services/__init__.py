"""
Portfolio Management Tool - Services Layer

This module provides services for:
- Database connectivity and query execution
- Market data fetching (Bloomberg, databases, Yahoo Finance)
- Position data management
- P&L calculation
- Risk metrics and Greeks calculation
- Bloomberg EMSX order management
- Compliance and regulatory data

Each service can integrate with the existing PyQt business logic from source/.

Note: finance_service.py module is deprecated. Use MarketDataService class instead.
"""

from app.services.database_service import DatabaseService
from app.services.market_data_service import MarketDataService
from app.services.position_service import PositionService
from app.services.pnl_service import PnLService
from app.services.risk_service import RiskService
from app.services.emsx_service import EMSXService
from app.services.notification_service import NotificationService
from app.services.user_service import UserService
from app.services.portfolio_service import PortfolioService
from app.services.compliance_service import ComplianceService

# Deprecated: finance_service module - use MarketDataService instead
from app.services import finance_service

__all__ = [
    "DatabaseService",
    "MarketDataService",
    "PositionService",
    "PnLService",
    "RiskService",
    "EMSXService",
    "NotificationService",
    "UserService",
    "PortfolioService",
    "ComplianceService",
    "finance_service",  # Deprecated - for backward compatibility only
]
