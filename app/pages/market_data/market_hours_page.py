import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.market_data.market_data_views import market_hours_table

MODULE_NAME = "Market Data"
SUBTAB_NAME = "Market Hours"
SUBTABS = [
    "Market Data",
    "FX Data",
    "Reference Data",
    "Historical Data",
    "Trading Calendar",
    "Market Hours",
]


def market_hours_page() -> rx.Component:
    return module_layout(
        content=market_hours_table(),
        module_name=MODULE_NAME,
        subtab_name=SUBTAB_NAME,
        subtabs=SUBTABS,
    )
