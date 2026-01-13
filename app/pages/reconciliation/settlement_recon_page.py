import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.reconciliation.reconciliation_views import settlement_recon_table
from app.states.ui.ui_state import UIState


def settlement_recon_page() -> rx.Component:
    return module_layout(
        settlement_recon_table(),
        "Recon",
        "Settlement Recon",
        UIState.MODULE_SUBTABS["Recon"],
    )
