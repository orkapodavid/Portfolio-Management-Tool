import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.portfolio_tools.coming_resets_ag_grid import coming_resets_ag_grid
from app.states.ui.ui_state import UIState


def coming_resets_page() -> rx.Component:
    return module_layout(
        coming_resets_ag_grid(),
        "Portfolio Tools",
        "Coming Resets",
        UIState.MODULE_SUBTABS["Portfolio Tools"],
    )
