import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.instruments.instrument_views import stock_screener_view
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def stock_screener_page() -> rx.Component:
    return module_layout(
        stock_screener_view(),
        "Instruments",
        "Stock Screener",
        PortfolioDashboardState.MODULE_SUBTABS["Instruments"],
    )
