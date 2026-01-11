import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.portfolio_tools.portfolio_tools_views import pay_to_hold_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def pay_to_hold_page() -> rx.Component:
    return module_layout(
        pay_to_hold_table(),
        "Portfolio Tools",
        "Pay-To-Hold",
        PortfolioDashboardState.MODULE_SUBTABS["Portfolio Tools"],
    )
