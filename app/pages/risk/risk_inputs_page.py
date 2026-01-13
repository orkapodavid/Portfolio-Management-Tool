import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.risk.risk_views import risk_inputs_table
from app.states.ui.ui_state import UIState


def risk_inputs_page() -> rx.Component:
    return module_layout(
        risk_inputs_table(),
        "Risk",
        "Risk Inputs",
        UIState.MODULE_SUBTABS["Risk"],
    )
