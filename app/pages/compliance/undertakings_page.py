import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.compliance.compliance_views import undertakings_table
from app.states.ui.ui_state import UIState


def undertakings_page() -> rx.Component:
    return module_layout(
        undertakings_table(),
        "Compliance",
        "Undertakings",
        UIState.MODULE_SUBTABS["Compliance"],
    )
