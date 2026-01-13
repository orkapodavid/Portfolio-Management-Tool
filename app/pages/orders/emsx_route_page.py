import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.emsx.emsx_views import emsa_route_table
from app.states.ui.ui_state import UIState


def emsx_route_page() -> rx.Component:
    return module_layout(
        emsa_route_table(),
        "Orders",
        "EMSX Route",
        UIState.MODULE_SUBTABS["Orders"],
    )
