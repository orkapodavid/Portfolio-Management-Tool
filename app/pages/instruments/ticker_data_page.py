import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.instruments.ticker_data_ag_grid import ticker_data_ag_grid
from app.states.ui.ui_state import UIState


def ticker_data_page() -> rx.Component:
    return module_layout(
        ticker_data_ag_grid(),
        "Instruments",
        "Ticker Data",
        UIState.MODULE_SUBTABS["Instruments"],
    )
