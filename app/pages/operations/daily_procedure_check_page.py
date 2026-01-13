import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.operations.operations_views import daily_procedure_check_table
from app.states.ui.ui_state import UIState


def daily_procedure_check_page() -> rx.Component:
    return module_layout(
        daily_procedure_check_table(),
        "Operations",
        "Daily Procedure Check",
        UIState.MODULE_SUBTABS["Operations"],
    )
