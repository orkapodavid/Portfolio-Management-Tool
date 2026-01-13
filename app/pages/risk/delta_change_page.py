import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.risk.risk_views import delta_change_table
from app.states.ui.ui_state import UIState


def delta_change_page() -> rx.Component:
    return module_layout(
        delta_change_table(),
        "Risk",
        "Delta Change",
        UIState.MODULE_SUBTABS["Risk"],
    )
