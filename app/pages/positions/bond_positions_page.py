import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.positions.bond_position_ag_grid import bond_position_ag_grid

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
        content=bond_position_ag_grid(),
        module_name=MODULE_NAME,
        subtab_name=SUBTAB_NAME,
        subtabs=SUBTABS,
    )
