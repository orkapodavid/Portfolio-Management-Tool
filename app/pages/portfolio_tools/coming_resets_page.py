import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.portfolio_tools.portfolio_tools_views import coming_resets_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def coming_resets_page() -> rx.Component:
    return module_layout(
        coming_resets_table(),
        "Portfolio Tools",
        "Coming Resets",
        PortfolioDashboardState.MODULE_SUBTABS["Portfolio Tools"],
    )
