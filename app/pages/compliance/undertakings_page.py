import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.compliance.compliance_views import undertakings_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def undertakings_page() -> rx.Component:
    return module_layout(
        undertakings_table(),
        "Compliance",
        "Undertakings",
        PortfolioDashboardState.MODULE_SUBTABS["Compliance"],
    )
