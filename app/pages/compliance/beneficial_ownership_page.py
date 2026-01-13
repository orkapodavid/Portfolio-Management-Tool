import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.compliance.compliance_views import beneficial_ownership_table
from app.states.ui.ui_state import UIState


def beneficial_ownership_page() -> rx.Component:
    return module_layout(
        beneficial_ownership_table(),
        "Compliance",
        "Beneficial Ownership",
        UIState.MODULE_SUBTABS["Compliance"],
    )
