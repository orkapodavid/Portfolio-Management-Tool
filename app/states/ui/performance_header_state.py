"""
Performance Header State - Dedicated state for the performance header component.

Handles:
- KPI metrics loading
- Top movers data
- Portfolio summary calculations
- Show/hide top movers toggle
"""

import reflex as rx
from typing import List
import logging

from app.states.types import KPIMetric, TopMover, Holding
from app.services import services

logger = logging.getLogger(__name__)


class PerformanceHeaderState(rx.State):
    """
    State for performance header component.

    Separated from UIState to follow the Mixin Per Tab pattern
    and ensure proper data loading via on_mount.
    """

    # KPI metrics
    kpi_metrics: List[KPIMetric] = []

    # Top movers data (5 categories)
    top_movers_ops: List[TopMover] = []
    top_movers_ytd: List[TopMover] = []
    top_movers_delta: List[TopMover] = []
    top_movers_price: List[TopMover] = []
    top_movers_volume: List[TopMover] = []

    # Portfolio holdings for summary cards
    portfolio_holdings: List[Holding] = []

    # UI state
    show_top_movers: bool = False
    is_loading: bool = False

    # Computed vars for portfolio summary
    @rx.var
    def portfolio_total_value(self) -> float:
        """Total portfolio value."""
        if not self.portfolio_holdings:
            return 0.0
        return sum([h["shares"] * h["current_price"] for h in self.portfolio_holdings])

    @rx.var
    def portfolio_total_cost_basis(self) -> float:
        """Total cost basis."""
        if not self.portfolio_holdings:
            return 0.0
        return sum([h["shares"] * h["avg_cost"] for h in self.portfolio_holdings])

    @rx.var
    def portfolio_total_gain_loss(self) -> float:
        """Total gain/loss."""
        return self.portfolio_total_value - self.portfolio_total_cost_basis

    @rx.var
    def portfolio_total_gain_loss_pct(self) -> float:
        """Total gain/loss percentage."""
        if self.portfolio_total_cost_basis == 0:
            return 0.0
        return self.portfolio_total_gain_loss / self.portfolio_total_cost_basis * 100

    @rx.var
    def portfolio_daily_change_value(self) -> float:
        """Daily change value."""
        if not self.portfolio_holdings:
            return 0.0
        return sum(
            [
                h["shares"] * h["current_price"] * (h["daily_change_pct"] / 100)
                for h in self.portfolio_holdings
            ]
        )

    @rx.event
    def toggle_top_movers(self):
        """Toggle the top movers section visibility."""
        self.show_top_movers = not self.show_top_movers

    @rx.event
    async def load_performance_data(self):
        """
        Load all performance header data.
        Called on_mount of the performance header component.
        """
        self.is_loading = True
        try:
            # Load KPI metrics (from core via PerformanceHeaderService)
            self.kpi_metrics = await services.performance_header.get_kpi_metrics()

            # Load top movers for all categories (from MarketDataService)
            self.top_movers_ops = await services.market_data.get_top_movers("ops")
            self.top_movers_ytd = await services.market_data.get_top_movers("ytd")
            self.top_movers_delta = await services.market_data.get_top_movers("delta")
            self.top_movers_price = await services.market_data.get_top_movers("price")
            self.top_movers_volume = await services.market_data.get_top_movers("volume")

            # Load portfolio holdings (from core via PerformanceHeaderService)
            self.portfolio_holdings = (
                await services.performance_header.get_portfolio_holdings()
            )

            logger.info("Performance header data loaded successfully")
        except Exception as e:
            logger.exception(f"Error loading performance header data: {e}")
        finally:
            self.is_loading = False
