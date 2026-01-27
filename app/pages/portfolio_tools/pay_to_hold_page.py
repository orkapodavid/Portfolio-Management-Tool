import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.portfolio_tools.pay_to_hold_ag_grid import pay_to_hold_ag_grid
from app.states.ui.ui_state import UIState


def pay_to_hold_page() -> rx.Component:
    return module_layout(
        pay_to_hold_ag_grid(),
        "Portfolio Tools",
        "Pay-To-Hold",
        UIState.MODULE_SUBTABS["Portfolio Tools"],
    )
