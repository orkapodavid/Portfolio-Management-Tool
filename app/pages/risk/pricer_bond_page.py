import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.risk.risk_views import pricer_bond_view
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def pricer_bond_page() -> rx.Component:
    return module_layout(
        pricer_bond_view(),
        "Risk",
        "Pricer Bond",
        PortfolioDashboardState.MODULE_SUBTABS["Risk"],
    )
