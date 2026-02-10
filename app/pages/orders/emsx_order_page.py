import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.emsx.emsx_order_ag_grid import emsx_order_ag_grid
from app.states.ui.ui_state import UIState


def emsx_order_page() -> rx.Component:
    return module_layout(
        emsx_order_ag_grid(),
        "Orders",
        "EMSX Order",
        UIState.MODULE_SUBTABS["Orders"],
    )