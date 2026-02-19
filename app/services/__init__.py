"""
Portfolio Management Tool - Services Layer

Re-exports all domain services for use by Reflex states.
Each service module is a pure re-export from pmt_core.
"""

from app.services.pnl.pnl_service import PnLService
from app.services.positions.position_service import PositionService
from app.services.risk.risk_service import RiskService
from app.services.compliance.compliance_service import ComplianceService
from app.services.portfolio_tools.portfolio_tools_service import PortfolioToolsService
from app.services.market_data.market_data_service import MarketDataService
from app.services.emsx.emsx_service import EMSXService
from app.services.notifications.notification_service import NotificationService
from app.services.notifications.notification_registry import NotificationRegistry
from app.services.user.user_service import UserService
from app.services.shared.performance_header_service import PerformanceHeaderService

from app.services.events.reverse_inquiry_service import ReverseInquiryService
from app.services.events.event_calendar_service import EventCalendarService
from app.services.events.event_stream_service import EventStreamService
from app.services.operations.operations_service import OperationsService
from app.services.instruments.instruments_service import InstrumentsService
from app.services.reconciliation.reconciliation_service import ReconciliationService
from app.services.registry import services

# Import notification providers to ensure registration at startup
import app.services.notifications.notification_providers  # noqa: F401

__all__ = [
    "services",
    "PnLService",
    "PositionService",
    "RiskService",
    "ComplianceService",
    "PortfolioToolsService",
    "MarketDataService",
    "EMSXService",
    "NotificationService",
    "NotificationRegistry",
    "UserService",
    "PerformanceHeaderService",
    "ReverseInquiryService",
    "EventCalendarService",
    "EventStreamService",
    "OperationsService",
    "InstrumentsService",
    "ReconciliationService",
]
