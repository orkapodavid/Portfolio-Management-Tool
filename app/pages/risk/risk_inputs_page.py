import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.risk.risk_views import risk_inputs_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def risk_inputs_page() -> rx.Component:
    return module_layout(
        risk_inputs_table(),
        "Risk",
        "Risk Inputs",
        PortfolioDashboardState.MODULE_SUBTABS["Risk"],
    )
