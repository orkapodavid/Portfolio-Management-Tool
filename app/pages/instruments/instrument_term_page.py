import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.instruments.instrument_views import instrument_term_table
from app.states.ui.ui_state import UIState


def instrument_term_page() -> rx.Component:
    return module_layout(
        instrument_term_table(),
        "Instruments",
        "Instrument Term",
        UIState.MODULE_SUBTABS["Instruments"],
    )
