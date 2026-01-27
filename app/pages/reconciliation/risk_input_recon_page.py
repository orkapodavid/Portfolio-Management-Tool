import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.reconciliation.risk_input_recon_ag_grid import risk_input_recon_ag_grid
from app.states.ui.ui_state import UIState


def risk_input_recon_page() -> rx.Component:
    return module_layout(
        risk_input_recon_ag_grid(),
        "Recon",
        "Risk Input Recon",
        UIState.MODULE_SUBTABS["Recon"],
    )
