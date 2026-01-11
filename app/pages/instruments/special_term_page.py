import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.instruments.instrument_views import special_term_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def special_term_page() -> rx.Component:
    return module_layout(
        special_term_table(),
        "Instruments",
        "Special Term",
        PortfolioDashboardState.MODULE_SUBTABS["Instruments"],
    )
