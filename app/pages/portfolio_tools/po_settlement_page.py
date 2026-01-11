import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.portfolio_tools.portfolio_tools_views import po_settlement_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def po_settlement_page() -> rx.Component:
    return module_layout(
        po_settlement_table(),
        "Portfolio Tools",
        "PO Settlement",
        PortfolioDashboardState.MODULE_SUBTABS["Portfolio Tools"],
    )
