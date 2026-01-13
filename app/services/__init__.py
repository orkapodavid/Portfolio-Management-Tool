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

"""Services layer - all domain services re-exported for convenience."""

from app.services.pnl.pnl_service import PnLService
from app.services.positions.position_service import PositionService
from app.services.risk.risk_service import RiskService
from app.services.compliance.compliance_service import ComplianceService
from app.services.portfolio.portfolio_service import PortfolioService
from app.services.market_data.market_data_service import MarketDataService
from app.services.emsx.emsx_service import EMSXService
from app.services.notifications.notification_service import NotificationService
from app.services.user.user_service import UserService
from app.services.shared.database_service import DatabaseService
from app.services.shared.finance_service import FinanceService

__all__ = [
    "PnLService",
    "PositionService",
    "RiskService",
    "ComplianceService",
    "PortfolioService",
    "MarketDataService",
    "EMSXService",
    "NotificationService",
    "UserService",
    "DatabaseService",
    "FinanceService",
]
