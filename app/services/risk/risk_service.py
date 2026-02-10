"""
Risk Service for Portfolio Management Tool.

Delegates core risk data methods to pmt_core.services.risk.RiskService.
Keeps notification providers in the app layer.
"""

import logging
from typing import Optional

from pmt_core.services.risk import RiskService as CoreRiskService
from pmt_core import RiskRecord

from app.ag_grid_constants import GridId
from app.services.notifications.notification_registry import NotificationRegistry
from app.services.notifications.notification_constants import (
    NotificationCategory,
    NotificationIcon,
    NotificationColor,
)

logger = logging.getLogger(__name__)


# === NOTIFICATION PROVIDERS ===
def _get_risk_notifications() -> list[dict]:
    """Mock risk notifications for delta/gamma exposure alerts."""
    return [
        {
            "id": "risk-001",
            "category": NotificationCategory.ALERTS,
            "title": "Risk Alert",
            "message": "Portfolio delta exposure has increased by 15%",
            "time_ago": "5 hours ago",
            "is_read": True,
            "icon": NotificationIcon.ALERT_TRIANGLE,
            "color": NotificationColor.RED,
            "module": "Risk",
            "subtab": "Delta Change",
            "row_id": "TSLA",
            "grid_id": GridId.DELTA_CHANGE,
            "ticker": "TSLA",
        },
    ]


# Register provider at module load
NotificationRegistry.register("risk", _get_risk_notifications)


class RiskService:
    """
    Service for risk metrics calculation and retrieval.
    Delegates to pmt_core RiskService for data.
    """

    def __init__(self):
        self.core_service = CoreRiskService()

    async def get_delta_changes(
        self, trade_date: Optional[str] = None
    ) -> list[RiskRecord]:
        """Get position delta changes. Delegates to core."""
        return await self.core_service.get_delta_changes(trade_date)

    async def get_risk_measures(
        self, trade_date: Optional[str] = None, simulation_num: Optional[int] = None
    ) -> list[RiskRecord]:
        """Get comprehensive risk measures. Delegates to core."""
        return await self.core_service.get_risk_measures(trade_date, simulation_num)

    async def get_gamma_exposure(self, trade_date: Optional[str] = None) -> list[dict]:
        """Get gamma exposure. Delegates to core."""
        return await self.core_service.get_gamma_exposure(trade_date)

    async def calculate_portfolio_var(
        self,
        portfolio_id: Optional[str] = None,
        confidence_level: float = 0.95,
        horizon_days: int = 1,
    ) -> dict:
        """Calculate VaR. Delegates to core."""
        return await self.core_service.calculate_portfolio_var(
            portfolio_id, confidence_level, horizon_days
        )

    async def get_risk_scenarios(self, scenario_type: str = "stress") -> list[dict]:
        """Run risk scenario analysis. Delegates to core."""
        return await self.core_service.get_risk_scenarios(scenario_type)

    async def get_risk_inputs(
        self, trade_date: Optional[str] = None
    ) -> list[RiskRecord]:
        """Get risk inputs. Delegates to core."""
        return await self.core_service.get_risk_inputs(trade_date)
