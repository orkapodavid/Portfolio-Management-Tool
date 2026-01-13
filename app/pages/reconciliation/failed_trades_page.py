import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.reconciliation.reconciliation_views import failed_trades_table
from app.states.ui.ui_state import UIState


def failed_trades_page() -> rx.Component:
    return module_layout(
        failed_trades_table(),
        "Recon",
        "Failed Trades",
        UIState.MODULE_SUBTABS["Recon"],
    )
