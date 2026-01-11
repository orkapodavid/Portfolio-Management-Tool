import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.instruments.instrument_views import instrument_data_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def instrument_data_page() -> rx.Component:
    return module_layout(
        instrument_data_table(),
        "Instruments",
        "Instrument Data",
        PortfolioDashboardState.MODULE_SUBTABS["Instruments"],
    )
