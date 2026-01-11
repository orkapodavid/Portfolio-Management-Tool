import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.portfolio_tools.portfolio_tools_views import cb_installments_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def cb_installments_page() -> rx.Component:
    return module_layout(
        cb_installments_table(),
        "Portfolio Tools",
        "CB Installments",
        PortfolioDashboardState.MODULE_SUBTABS["Portfolio Tools"],
    )
