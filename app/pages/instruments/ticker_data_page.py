import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.instruments.instrument_views import ticker_data_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def ticker_data_page() -> rx.Component:
    return module_layout(
        ticker_data_table(),
        "Instruments",
        "Ticker Data",
        PortfolioDashboardState.MODULE_SUBTABS["Instruments"],
    )
