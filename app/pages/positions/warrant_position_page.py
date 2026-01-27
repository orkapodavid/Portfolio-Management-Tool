import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.positions.warrant_position_ag_grid import warrant_position_ag_grid

MODULE_NAME = "Positions"
SUBTAB_NAME = "Warrant Position"
SUBTABS = [
    "Positions",
    "Stock Position",
    "Warrant Position",
    "Bond Positions",
    "Trade Summary",
]


def warrant_position_page() -> rx.Component:
    return module_layout(
        content=warrant_position_ag_grid(),
        module_name=MODULE_NAME,
        subtab_name=SUBTAB_NAME,
        subtabs=SUBTABS,
    )
