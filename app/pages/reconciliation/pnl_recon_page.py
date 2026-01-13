import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.reconciliation.reconciliation_views import pnl_recon_table
from app.states.ui.ui_state import UIState


def pnl_recon_page() -> rx.Component:
    return module_layout(
        pnl_recon_table(),
        "Recon",
        "PnL Recon",
        UIState.MODULE_SUBTABS["Recon"],
    )
