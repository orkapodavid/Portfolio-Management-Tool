import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.portfolio_tools.deal_indication_ag_grid import deal_indication_ag_grid
from app.states.ui.ui_state import UIState


def deal_indication_page() -> rx.Component:
    return module_layout(
        deal_indication_ag_grid(),
        "Portfolio Tools",
        "Deal Indication",
        UIState.MODULE_SUBTABS["Portfolio Tools"],
    )
