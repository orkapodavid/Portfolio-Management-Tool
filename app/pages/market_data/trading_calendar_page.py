import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.market_data.trading_calendar_ag_grid import trading_calendar_ag_grid

MODULE_NAME = "Market Data"
SUBTAB_NAME = "Trading Calendar"
SUBTABS = [
    "Market Data",
    "FX Data",
    "Reference Data",
    "Historical Data",
    "Trading Calendar",
    "Market Hours",
]


def trading_calendar_page() -> rx.Component:
    return module_layout(
        content=trading_calendar_ag_grid(),
        module_name=MODULE_NAME,
        subtab_name=SUBTAB_NAME,
        subtabs=SUBTABS,
    )
