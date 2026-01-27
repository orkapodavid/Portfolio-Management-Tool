import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.positions.trade_summary_ag_grid import trade_summary_ag_grid

MODULE_NAME = "Positions"
SUBTAB_NAME = "Trade Summary"
SUBTABS = [
    "Positions",
    "Stock Position",
    "Warrant Position",
    "Bond Positions",
    "Trade Summary",
]


def trade_summary_page() -> rx.Component:
    return module_layout(
        content=trade_summary_ag_grid(),
        module_name=MODULE_NAME,
        subtab_name=SUBTAB_NAME,
        subtabs=SUBTABS,
    )
