import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.portfolio_tools.reset_dates_ag_grid import reset_dates_ag_grid
from app.states.ui.ui_state import UIState


def reset_dates_page() -> rx.Component:
    return module_layout(
        reset_dates_ag_grid(),
        "Portfolio Tools",
        "Reset Dates",
        UIState.MODULE_SUBTABS["Portfolio Tools"],
    )
