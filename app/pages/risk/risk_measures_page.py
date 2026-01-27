import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.risk.risk_measures_ag_grid import risk_measures_ag_grid
from app.states.ui.ui_state import UIState


def risk_measures_page() -> rx.Component:
    return module_layout(
        risk_measures_ag_grid(),
        "Risk",
        "Risk Measures",
        UIState.MODULE_SUBTABS["Risk"],
    )
