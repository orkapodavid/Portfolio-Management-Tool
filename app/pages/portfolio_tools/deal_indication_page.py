import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.portfolio_tools.portfolio_tools_views import deal_indication_table
from app.states.ui.ui_state import UIState


def deal_indication_page() -> rx.Component:
    return module_layout(
        deal_indication_table(),
        "Portfolio Tools",
        "Deal Indication",
        UIState.MODULE_SUBTABS["Portfolio Tools"],
    )
