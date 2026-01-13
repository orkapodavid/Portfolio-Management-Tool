import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.emsx.emsx_views import emsa_order_table
from app.states.ui.ui_state import UIState


def emsx_order_page() -> rx.Component:
    return module_layout(
        emsa_order_table(),
        "Orders",
        "EMSX Order",
        UIState.MODULE_SUBTABS["Orders"],
    )
