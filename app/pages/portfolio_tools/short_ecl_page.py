import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.portfolio_tools.portfolio_tools_views import short_ecl_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def short_ecl_page() -> rx.Component:
    return module_layout(
        short_ecl_table(),
        "Portfolio Tools",
        "Short ECL",
        PortfolioDashboardState.MODULE_SUBTABS["Portfolio Tools"],
    )
