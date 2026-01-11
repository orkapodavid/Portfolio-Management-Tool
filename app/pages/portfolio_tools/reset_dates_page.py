import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.portfolio_tools.portfolio_tools_views import reset_dates_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def reset_dates_page() -> rx.Component:
    return module_layout(
        reset_dates_table(),
        "Portfolio Tools",
        "Reset Dates",
        PortfolioDashboardState.MODULE_SUBTABS["Portfolio Tools"],
    )
