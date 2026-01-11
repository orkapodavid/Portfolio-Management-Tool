import reflex as rx
from app.components.shared.module_layout import module_layout
from app.components.instruments.instrument_views import ticker_data_table

MODULE_NAME = "Market Data"
SUBTAB_NAME = "Reference Data"
SUBTABS = [
    "Market Data",
    "FX Data",
    "Reference Data",
    "Historical Data",
    "Trading Calendar",
    "Market Hours",
]


def ticker_data_page() -> rx.Component:
    return module_layout(
        content=ticker_data_table(),
        module_name=MODULE_NAME,
        subtab_name=SUBTAB_NAME,
        subtabs=SUBTABS,
    )
