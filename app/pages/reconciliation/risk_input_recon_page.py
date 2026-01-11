import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.reconciliation.reconciliation_views import risk_input_recon_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def risk_input_recon_page() -> rx.Component:
    return module_layout(
        risk_input_recon_table(),
        "Recon",
        "Risk Input Recon",
        PortfolioDashboardState.MODULE_SUBTABS["Recon"],
    )
