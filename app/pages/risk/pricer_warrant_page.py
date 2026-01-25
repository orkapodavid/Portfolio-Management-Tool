import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.risk.pricer_warrant_view import pricer_warrant_view
from app.states.ui.ui_state import UIState


def pricer_warrant_page() -> rx.Component:
    return module_layout(
        pricer_warrant_view(),
        "Risk",
        "Pricer Warrant",
        UIState.MODULE_SUBTABS["Risk"],
    )
