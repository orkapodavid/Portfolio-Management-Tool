import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.reconciliation.reconciliation_views import failed_trades_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def failed_trades_page() -> rx.Component:
    return module_layout(
        failed_trades_table(),
        "Recon",
        "Failed Trades",
        PortfolioDashboardState.MODULE_SUBTABS["Recon"],
    )
