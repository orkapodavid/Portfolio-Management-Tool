import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.market_data.fx_data_ag_grid import fx_data_ag_grid

MODULE_NAME = "Market Data"
SUBTAB_NAME = "FX Data"
SUBTABS = [
    "Market Data",
    "FX Data",
    "Reference Data",
    "Historical Data",
    "Trading Calendar",
    "Market Hours",
]


def fx_data_page() -> rx.Component:
    return module_layout(
        content=fx_data_ag_grid(),
        module_name=MODULE_NAME,
        subtab_name=SUBTAB_NAME,
        subtabs=SUBTABS,
    )
