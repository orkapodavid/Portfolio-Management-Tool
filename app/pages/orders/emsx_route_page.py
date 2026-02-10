import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.emsx.emsx_route_ag_grid import emsx_route_ag_grid
from app.states.ui.ui_state import UIState


def emsx_route_page() -> rx.Component:
    return module_layout(
        emsx_route_ag_grid(),
        "Orders",
        "EMSX Route",
        UIState.MODULE_SUBTABS["Orders"],
    )