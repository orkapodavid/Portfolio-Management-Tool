import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.operations.operations_views import daily_procedure_check_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def daily_procedure_check_page() -> rx.Component:
    return module_layout(
        daily_procedure_check_table(),
        "Operations",
        "Daily Procedure Check",
        PortfolioDashboardState.MODULE_SUBTABS["Operations"],
    )
