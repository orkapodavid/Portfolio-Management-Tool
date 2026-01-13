import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.events.events_views import reverse_inquiry_view
from app.states.ui.ui_state import UIState


def reverse_inquiry_page() -> rx.Component:
    return module_layout(
        reverse_inquiry_view(),
        "Events",
        "Reverse Inquiry",
        UIState.MODULE_SUBTABS["Events"],
    )
