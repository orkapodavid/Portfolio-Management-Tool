import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.instruments.instrument_views import stock_screener_view
from app.states.ui.ui_state import UIState


def stock_screener_page() -> rx.Component:
    return module_layout(
        stock_screener_view(),
        "Instruments",
        "Stock Screener",
        UIState.MODULE_SUBTABS["Instruments"],
    )
