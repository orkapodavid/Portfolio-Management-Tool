import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.compliance.undertakings_ag_grid import undertakings_ag_grid
from app.states.ui.ui_state import UIState


def undertakings_page() -> rx.Component:
    return module_layout(
        undertakings_ag_grid(),
        "Compliance",
        "Undertakings",
        UIState.MODULE_SUBTABS["Compliance"],
    )
