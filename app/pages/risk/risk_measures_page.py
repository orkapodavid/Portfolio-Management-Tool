import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.risk.risk_views import risk_measures_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def risk_measures_page() -> rx.Component:
    return module_layout(
        risk_measures_table(),
        "Risk",
        "Risk Measures",
        PortfolioDashboardState.MODULE_SUBTABS["Risk"],
    )
