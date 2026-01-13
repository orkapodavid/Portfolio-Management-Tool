import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.instruments.instrument_views import special_term_table
from app.states.ui.ui_state import UIState


def special_term_page() -> rx.Component:
    return module_layout(
        special_term_table(),
        "Instruments",
        "Special Term",
        UIState.MODULE_SUBTABS["Instruments"],
    )
