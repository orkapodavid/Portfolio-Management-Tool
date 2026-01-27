import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.instruments.instrument_data_ag_grid import instrument_data_ag_grid
from app.states.ui.ui_state import UIState


def instrument_data_page() -> rx.Component:
    return module_layout(
        instrument_data_ag_grid(),
        "Instruments",
        "Instrument Data",
        UIState.MODULE_SUBTABS["Instruments"],
    )
