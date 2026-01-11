import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.compliance.compliance_views import monthly_exercise_limit_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def monthly_exercise_limit_page() -> rx.Component:
    return module_layout(
        monthly_exercise_limit_table(),
        "Compliance",
        "Monthly Exercise Limit",
        PortfolioDashboardState.MODULE_SUBTABS["Compliance"],
    )
