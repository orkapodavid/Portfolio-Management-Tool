import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.compliance.compliance_views import restricted_list_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def restricted_list_page() -> rx.Component:
    return module_layout(
        restricted_list_table(),
        "Compliance",
        "Restricted List",
        PortfolioDashboardState.MODULE_SUBTABS["Compliance"],
    )
