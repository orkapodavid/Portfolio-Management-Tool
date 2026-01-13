import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.reconciliation.reconciliation_views import pps_recon_table
from app.states.ui.ui_state import UIState


def pps_recon_page() -> rx.Component:
    return module_layout(
        pps_recon_table(),
        "Recon",
        "PPS Recon",
        UIState.MODULE_SUBTABS["Recon"],
    )
