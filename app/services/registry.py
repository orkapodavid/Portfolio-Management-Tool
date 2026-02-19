"""
Service Registry — Singleton access to all domain services.

Provides lazily-instantiated, module-level singleton service instances
via cached properties. Each service is allocated once on first access
and reused for the lifetime of the process.

Usage:
    from app.services.registry import services
    data = await services.pnl.get_pnl_changes(date)
"""

from functools import cached_property


class ServiceRegistry:
    """
    Centralized singleton registry for all domain services.

    Each service is lazily instantiated via @cached_property —
    allocated once on first access, reused thereafter.

    Imports are deferred inside properties to avoid circular imports
    and to keep startup fast.
    """

    @cached_property
    def pnl(self):
        from pmt_core.services.pnl import PnLService

        return PnLService()

    @cached_property
    def positions(self):
        from pmt_core.services.positions import PositionService

        return PositionService()

    @cached_property
    def risk(self):
        from pmt_core.services.risk import RiskService

        return RiskService()

    @cached_property
    def compliance(self):
        from pmt_core.services.compliance import ComplianceService

        return ComplianceService()

    @cached_property
    def portfolio_tools(self):
        from pmt_core.services.portfolio_tools import PortfolioToolsService

        return PortfolioToolsService()

    @cached_property
    def market_data(self):
        from pmt_core.services.market_data import MarketDataService

        return MarketDataService()

    @cached_property
    def emsx(self):
        from pmt_core.services.emsx import EMSXService

        return EMSXService()

    @cached_property
    def operations(self):
        from pmt_core.services.operations import OperationsService

        return OperationsService()

    @cached_property
    def reconciliation(self):
        from pmt_core.services.reconciliation import ReconciliationService

        return ReconciliationService()

    @cached_property
    def user(self):
        from pmt_core.services.user import UserService

        return UserService()

    @cached_property
    def instruments(self):
        from pmt_core.services.instruments import InstrumentsService

        return InstrumentsService()

    @cached_property
    def reverse_inquiry(self):
        from pmt_core.services.events import ReverseInquiryService

        return ReverseInquiryService()

    @cached_property
    def event_calendar(self):
        from pmt_core.services.events import EventCalendarService

        return EventCalendarService()

    @cached_property
    def event_stream(self):
        from pmt_core.services.events import EventStreamService

        return EventStreamService()

    @cached_property
    def performance_header(self):
        from pmt_core.services.performance import PerformanceService

        return PerformanceService()

    @cached_property
    def notifications(self):
        from pmt_core.services.notifications import NotificationService

        return NotificationService()

    @cached_property
    def notification_registry(self):
        from pmt_core.services.notifications import NotificationRegistry

        return NotificationRegistry()


# Module-level singleton — import this
services = ServiceRegistry()
