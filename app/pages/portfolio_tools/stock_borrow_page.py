import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.portfolio_tools.stock_borrow_ag_grid import stock_borrow_ag_grid
from app.states.ui.ui_state import UIState


def stock_borrow_page() -> rx.Component:
    return module_layout(
        stock_borrow_ag_grid(),
        "Portfolio Tools",
        "Stock Borrow",
        UIState.MODULE_SUBTABS["Portfolio Tools"],
    )
