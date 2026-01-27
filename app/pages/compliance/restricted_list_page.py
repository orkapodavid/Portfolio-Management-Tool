import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.compliance.restricted_list_ag_grid import restricted_list_ag_grid
from app.states.ui.ui_state import UIState


def restricted_list_page() -> rx.Component:
    return module_layout(
        restricted_list_ag_grid(),
        "Compliance",
        "Restricted List",
        UIState.MODULE_SUBTABS["Compliance"],
    )
