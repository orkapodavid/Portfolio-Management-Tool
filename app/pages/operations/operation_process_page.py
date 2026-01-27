import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.operations.operation_process_ag_grid import operation_process_ag_grid
from app.states.ui.ui_state import UIState


def operation_process_page() -> rx.Component:
    return module_layout(
        operation_process_ag_grid(),
        "Operations",
        "Operation Process",
        UIState.MODULE_SUBTABS["Operations"],
    )
