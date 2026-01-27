import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.risk.delta_change_ag_grid import delta_change_ag_grid
from app.states.ui.ui_state import UIState


def delta_change_page() -> rx.Component:
    return module_layout(
        delta_change_ag_grid(),
        "Risk",
        "Delta Change",
        UIState.MODULE_SUBTABS["Risk"],
    )
