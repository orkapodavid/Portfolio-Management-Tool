import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.compliance.monthly_exercise_limit_ag_grid import monthly_exercise_limit_ag_grid
from app.states.ui.ui_state import UIState


def monthly_exercise_limit_page() -> rx.Component:
    return module_layout(
        monthly_exercise_limit_ag_grid(),
        "Compliance",
        "Monthly Exercise Limit",
        UIState.MODULE_SUBTABS["Compliance"],
    )
