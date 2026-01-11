import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.pnl.pnl_views import pnl_full_table

MODULE_NAME = "PnL"
SUBTAB_NAME = "PnL Full"
SUBTABS = ["PnL Change", "PnL Full", "PnL Summary", "PnL Currency"]


def pnl_full_page() -> rx.Component:
    return module_layout(
        content=pnl_full_table(),
        module_name=MODULE_NAME,
        subtab_name=SUBTAB_NAME,
        subtabs=SUBTABS,
    )
