"""
FX Data Table Component.

Displays foreign exchange rate data.
"""

import reflex as rx
from app.states.market_data.market_data_state import MarketDataState
from app.states.market_data.types import FXDataItem
from app.components.market_data.table_components import header_cell, text_cell


def fx_data_row(item: FXDataItem) -> rx.Component:
    """Render a single FX data row."""
    return rx.el.tr(
        text_cell(item["ticker"]),
        text_cell(item["last_price"]),
        text_cell(item["bid"]),
        text_cell(item["ask"]),
        text_cell(item["created_by"]),
        text_cell(item["created_time"]),
        text_cell(item["updated_by"]),
        text_cell(item["update"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def fx_data_table() -> rx.Component:
    """
    FX Data table component.

    Displays:
    - Ticker, Last Price, Bid, Ask
    - Created/Updated timestamps
    """
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Ticker"),
                    header_cell("Last Price"),
                    header_cell("Bid"),
                    header_cell("Ask"),
                    header_cell("Created by"),
                    header_cell("Created Time"),
                    header_cell("Updated by"),
                    header_cell("Update"),
                )
            ),
            rx.el.tbody(rx.foreach(MarketDataState.filtered_fx_data, fx_data_row)),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )
