"""
App Header State — KPI metrics and key items data.

Provides demo data for the app header component.
Generalized from PMT's PerformanceHeaderState for use in any app.
"""

import reflex as rx
from typing import List
from starter_app.states.ui.types import KPIMetric, TopMover


class AppHeaderState(rx.State):
    """State for the app header KPI strip and key items."""

    show_top_items: bool = False

    # Demo KPI Data — generalized app metrics
    kpi_metrics: List[KPIMetric] = [
        {
            "label": "Users",
            "value": "2,847",
            "is_positive": True,
            "trend_data": "0,5 10,12 20,8 30,15 40,20 50,18",
        },
        {
            "label": "Revenue",
            "value": "$124.5K",
            "is_positive": True,
            "trend_data": "0,12 10,8 20,15 30,10 40,18 50,14",
        },
        {
            "label": "Uptime",
            "value": "99.97%",
            "is_positive": True,
            "trend_data": "0,22 10,22 20,21 30,22 40,22 50,22",
        },
        {
            "label": "Avg Response",
            "value": "142ms",
            "is_positive": False,
            "trend_data": "0,18 10,15 20,20 30,22 40,19 50,24",
        },
    ]

    # App summary values
    app_total_requests: float = 1250000.00
    app_daily_requests: float = 12500.00
    app_success_rate: float = 99.85
    app_error_count: float = 18.00

    # Key items (replaces top movers)
    top_items_a: List[TopMover] = [
        {"ticker": "/api/users", "value": "2.4K rps", "change": "+12%", "is_positive": True},
        {"ticker": "/api/orders", "value": "1.8K rps", "change": "+8%", "is_positive": True},
        {"ticker": "/api/search", "value": "950 rps", "change": "-3%", "is_positive": False},
    ]

    top_items_b: List[TopMover] = [
        {"ticker": "/api/auth", "value": "320 rps", "change": "+5%", "is_positive": True},
        {"ticker": "/api/reports", "value": "180 rps", "change": "+22%", "is_positive": True},
        {"ticker": "/api/export", "value": "45 rps", "change": "-15%", "is_positive": False},
    ]

    @rx.event
    def toggle_top_items(self):
        self.show_top_items = not self.show_top_items

    @rx.event
    def load_header_data(self):
        """Load header data. Demo data is already set via defaults."""
        pass
