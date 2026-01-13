import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.portfolio_tools.portfolio_tools_views import po_settlement_table
from app.states.ui.ui_state import UIState


def po_settlement_page() -> rx.Component:
    return module_layout(
        po_settlement_table(),
        "Portfolio Tools",
        "PO Settlement",
        UIState.MODULE_SUBTABS["Portfolio Tools"],
    )
