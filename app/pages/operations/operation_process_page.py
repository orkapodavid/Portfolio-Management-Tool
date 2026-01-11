import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.operations.operations_views import operation_process_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def operation_process_page() -> rx.Component:
    return module_layout(
        operation_process_table(),
        "Operations",
        "Operation Process",
        PortfolioDashboardState.MODULE_SUBTABS["Operations"],
    )
