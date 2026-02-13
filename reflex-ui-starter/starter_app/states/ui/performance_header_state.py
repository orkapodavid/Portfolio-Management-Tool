"""
Performance Header State - KPI metrics and top movers data

Provides demo data for the performance header component.
"""

import reflex as rx
from typing import List
from starter_app.states.ui.types import KPIMetric, TopMover


class PerformanceHeaderState(rx.State):
    """State for the performance header KPI strip and top movers."""

    show_top_movers: bool = False

    # Demo KPI Data
    kpi_metrics: List[KPIMetric] = [
        {
            "label": "Revenue",
            "value": "$124.5K",
            "is_positive": True,
            "trend_data": "0,12 10,8 20,15 30,10 40,18 50,14",
        },
        {
            "label": "Users",
            "value": "2,847",
            "is_positive": True,
            "trend_data": "0,5 10,12 20,8 30,15 40,20 50,18",
        },
        {
            "label": "Bounce Rate",
            "value": "32.1%",
            "is_positive": False,
            "trend_data": "0,18 10,15 20,20 30,22 40,19 50,24",
        },
        {
            "label": "Avg Session",
            "value": "4m 32s",
            "is_positive": True,
            "trend_data": "0,8 10,10 20,12 30,9 40,14 50,16",
        },
    ]

    # Demo portfolio values
    portfolio_total_value: float = 1250000.00
    portfolio_daily_change_value: float = 12500.00
    portfolio_total_gain_loss: float = 85000.00
    portfolio_total_gain_loss_pct: float = 7.30

    # Demo top movers
    top_movers_a: List[TopMover] = [
        {"ticker": "AAPL", "value": "$195.20", "change": "+2.3%", "is_positive": True},
        {"ticker": "MSFT", "value": "$420.10", "change": "+1.8%", "is_positive": True},
        {"ticker": "GOOGL", "value": "$175.50", "change": "-0.5%", "is_positive": False},
    ]

    top_movers_b: List[TopMover] = [
        {"ticker": "TSLA", "value": "$248.30", "change": "+4.1%", "is_positive": True},
        {"ticker": "NVDA", "value": "$880.20", "change": "+3.2%", "is_positive": True},
        {"ticker": "META", "value": "$510.40", "change": "-1.2%", "is_positive": False},
    ]

    @rx.event
    def toggle_top_movers(self):
        self.show_top_movers = not self.show_top_movers

    @rx.event
    def load_performance_data(self):
        """Load performance data. Demo data is already set via defaults."""
        pass
