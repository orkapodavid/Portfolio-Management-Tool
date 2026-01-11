import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.positions.positions_views import bond_position_table

MODULE_NAME = "Positions"
SUBTAB_NAME = "Bond Positions"
SUBTABS = [
    "Positions",
    "Stock Position",
    "Warrant Position",
    "Bond Positions",
    "Trade Summary",
]


def bond_positions_page() -> rx.Component:
    return module_layout(
        content=bond_position_table(),
        module_name=MODULE_NAME,
        subtab_name=SUBTAB_NAME,
        subtabs=SUBTABS,
    )
