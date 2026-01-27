import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.pnl.pnl_full_ag_grid import pnl_full_ag_grid

MODULE_NAME = "PnL"
SUBTAB_NAME = "PnL Full"
SUBTABS = ["PnL Change", "PnL Full", "PnL Summary", "PnL Currency"]


def pnl_full_page() -> rx.Component:
    return module_layout(
        content=pnl_full_ag_grid(),
        module_name=MODULE_NAME,
        subtab_name=SUBTAB_NAME,
        subtabs=SUBTABS,
    )
