import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.instruments.instrument_views import instrument_data_table
from app.states.ui.ui_state import UIState


def instrument_data_page() -> rx.Component:
    return module_layout(
        instrument_data_table(),
        "Instruments",
        "Instrument Data",
        UIState.MODULE_SUBTABS["Instruments"],
    )
