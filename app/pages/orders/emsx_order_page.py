import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.emsa.emsa_views import emsa_order_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def emsx_order_page() -> rx.Component:
    return module_layout(
        emsa_order_table(),
        "Orders",
        "EMSX Order",
        PortfolioDashboardState.MODULE_SUBTABS["Orders"],
    )
