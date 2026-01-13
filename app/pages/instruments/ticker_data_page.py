import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.instruments.instrument_views import ticker_data_table
from app.states.ui.ui_state import UIState


def ticker_data_page() -> rx.Component:
    return module_layout(
        ticker_data_table(),
        "Instruments",
        "Ticker Data",
        UIState.MODULE_SUBTABS["Instruments"],
    )
