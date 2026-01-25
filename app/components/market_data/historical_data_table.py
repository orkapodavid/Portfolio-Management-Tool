"""
Historical Data Table Component.

Displays historical price and volume data.
"""

import reflex as rx
from app.states.market_data.market_data_state import MarketDataState
from app.states.market_data.types import HistoricalDataItem
from app.components.market_data.table_components import header_cell, text_cell


def historical_row(item: HistoricalDataItem) -> rx.Component:
    """Render a single historical data row."""
    return rx.el.tr(
        text_cell(item["trade_date"]),
        text_cell(item["ticker"]),
        text_cell(item["vwap_price"]),
        text_cell(item["last_price"]),
        text_cell(item["last_volume"]),
        text_cell(item["chg_1d_pct"]),
        text_cell(item["created_by"]),
        text_cell(item["created_time"]),
        text_cell(item["updated_by"]),
        text_cell(item["update"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def historical_data_table() -> rx.Component:
    """
    Historical Data table component.

    Displays:
    - Trade Date, Ticker
    - vWAP Price, Last Price, Last Volume
    - 1D Change %, timestamps
    """
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Trade Date"),
                    header_cell("Ticker"),
                    header_cell("vWAP Price"),
                    header_cell("Last Price"),
                    header_cell("Last Volume"),
                    header_cell("1D Change %"),
                    header_cell("Created By"),
                    header_cell("Created Time"),
                    header_cell("Updated By"),
                    header_cell("Update"),
                )
            ),
            rx.el.tbody(
                rx.foreach(MarketDataState.filtered_historical_data, historical_row)
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )
