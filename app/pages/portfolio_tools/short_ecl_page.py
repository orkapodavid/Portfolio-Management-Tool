import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.portfolio_tools.portfolio_tools_views import short_ecl_table
from app.states.ui.ui_state import UIState


def short_ecl_page() -> rx.Component:
    return module_layout(
        short_ecl_table(),
        "Portfolio Tools",
        "Short ECL",
        UIState.MODULE_SUBTABS["Portfolio Tools"],
    )
