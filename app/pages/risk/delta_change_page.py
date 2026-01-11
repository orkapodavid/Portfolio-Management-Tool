import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.risk.risk_views import delta_change_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def delta_change_page() -> rx.Component:
    return module_layout(
        delta_change_table(),
        "Risk",
        "Delta Change",
        PortfolioDashboardState.MODULE_SUBTABS["Risk"],
    )
