import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.portfolio_tools.portfolio_tools_views import stock_borrow_table
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState


def stock_borrow_page() -> rx.Component:
    return module_layout(
        stock_borrow_table(),
        "Portfolio Tools",
        "Stock Borrow",
        PortfolioDashboardState.MODULE_SUBTABS["Portfolio Tools"],
    )
