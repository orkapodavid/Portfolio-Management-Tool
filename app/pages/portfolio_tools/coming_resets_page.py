import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.portfolio_tools.portfolio_tools_views import coming_resets_table
from app.states.ui.ui_state import UIState


def coming_resets_page() -> rx.Component:
    return module_layout(
        coming_resets_table(),
        "Portfolio Tools",
        "Coming Resets",
        UIState.MODULE_SUBTABS["Portfolio Tools"],
    )
