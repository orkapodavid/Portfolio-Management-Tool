import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.risk.risk_inputs_ag_grid import risk_inputs_ag_grid
from app.states.ui.ui_state import UIState


def risk_inputs_page() -> rx.Component:
    return module_layout(
        risk_inputs_ag_grid(),
        "Risk",
        "Risk Inputs",
        UIState.MODULE_SUBTABS["Risk"],
    )
