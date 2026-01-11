import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.events.events_views import reverse_inquiry_view
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def reverse_inquiry_page() -> rx.Component:
    return module_layout(
        reverse_inquiry_view(),
        "Events",
        "Reverse Inquiry",
        PortfolioDashboardState.MODULE_SUBTABS["Events"],
    )
