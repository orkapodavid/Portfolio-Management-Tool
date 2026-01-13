import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.portfolio_tools.portfolio_tools_views import excess_amount_table
from app.states.ui.ui_state import UIState


def excess_amount_page() -> rx.Component:
    return module_layout(
        excess_amount_table(),
        "Portfolio Tools",
        "Excess Amount",
        UIState.MODULE_SUBTABS["Portfolio Tools"],
    )
