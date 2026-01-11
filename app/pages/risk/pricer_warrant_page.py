import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.risk.risk_views import pricer_warrant_view
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def pricer_warrant_page() -> rx.Component:
    return module_layout(
        pricer_warrant_view(),
        "Risk",
        "Pricer Warrant",
        PortfolioDashboardState.MODULE_SUBTABS["Risk"],
    )
