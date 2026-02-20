"""
Dashboard State — Main composed state for the Dashboard module.

Inherits from all Dashboard subtab mixins.
"""

import reflex as rx
from starter_app.states.dashboard.mixins.overview_mixin import OverviewMixin
from starter_app.states.dashboard.mixins.analytics_mixin import AnalyticsMixin


class DashboardState(
    OverviewMixin,
    AnalyticsMixin,
    rx.State,
):
    """
    Main Dashboard module state.
    Inherits from all Dashboard subtab mixins.
    """

    active_dashboard_subtab: str = "Overview"

    @rx.event
    async def load_dashboard_module_data(self):
        """Load data for the active subtab."""
        if self.active_dashboard_subtab == "Overview":
            yield type(self).load_overview_data
        elif self.active_dashboard_subtab == "Analytics":
            yield type(self).load_analytics_data

    @rx.event
    def set_dashboard_subtab(self, subtab: str):
        """Set the active dashboard subtab."""
        self.active_dashboard_subtab = subtab
