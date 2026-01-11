import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.events.events_views import event_calendar_view
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def event_calendar_page() -> rx.Component:
    return module_layout(
        event_calendar_view(),
        "Events",
        "Event Calendar",
        PortfolioDashboardState.MODULE_SUBTABS["Events"],
    )
