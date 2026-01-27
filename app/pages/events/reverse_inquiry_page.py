import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.events.reverse_inquiry_ag_grid import reverse_inquiry_ag_grid
from app.states.ui.ui_state import UIState


def reverse_inquiry_page() -> rx.Component:
    return module_layout(
        reverse_inquiry_ag_grid(),
        "Events",
        "Reverse Inquiry",
        UIState.MODULE_SUBTABS["Events"],
    )
