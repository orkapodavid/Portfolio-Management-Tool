import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.reconciliation.reconciliation_views import settlement_recon_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def settlement_recon_page() -> rx.Component:
    return module_layout(
        settlement_recon_table(),
        "Recon",
        "Settlement Recon",
        PortfolioDashboardState.MODULE_SUBTABS["Recon"],
    )
