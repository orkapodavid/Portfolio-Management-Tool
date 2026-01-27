import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.portfolio_tools.excess_amount_ag_grid import excess_amount_ag_grid
from app.states.ui.ui_state import UIState


def excess_amount_page() -> rx.Component:
    return module_layout(
        excess_amount_ag_grid(),
        "Portfolio Tools",
        "Excess Amount",
        UIState.MODULE_SUBTABS["Portfolio Tools"],
    )
