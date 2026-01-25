"""
Market Data Table Component.

Displays real-time market data with ticker prices, volumes, and status.
"""

import reflex as rx
from app.states.market_data.market_data_state import MarketDataState
from app.states.market_data.types import MarketDataItem
from app.components.market_data.table_components import header_cell, text_cell


def market_data_row(item: MarketDataItem) -> rx.Component:
    """Render a single market data row."""
    return rx.el.tr(
        text_cell(item["ticker"], clickable=True),
        text_cell(item["listed_shares"]),
        text_cell(item["last_volume"]),
        text_cell(item["last_price"]),
        text_cell(item["vwap_price"]),
        text_cell(item["bid"]),
        text_cell(item["ask"]),
        text_cell(item["chg_1d_pct"]),
        text_cell(item["implied_vol_pct"]),
        text_cell(item["market_status"]),
        text_cell(item["created_by"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def market_data_table() -> rx.Component:
    """
    Market Data table component.

    Displays:
    - Ticker, Listed Shares, Last Volume
    - Last Price, vWAP Price, Bid, Ask
    - 1D Change %, Implied Vol %, Market Status
    """
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Ticker", column_key="ticker"),
                    header_cell("Listed Shares (mm)", column_key="listed_shares"),
                    header_cell("Last Volume", column_key="last_volume"),
                    header_cell("Last Price", column_key="last_price"),
                    header_cell("vWAP Price", column_key="vwap_price"),
                    header_cell("Bid", column_key="bid"),
                    header_cell("Ask", column_key="ask"),
                    header_cell("1D Change %", column_key="chg_1d_pct"),
                    header_cell("Implied Vol %", column_key="implied_vol_pct"),
                    header_cell("Market Status", column_key="market_status"),
                    header_cell("Created by", column_key="created_by"),
                )
            ),
            rx.el.tbody(
                rx.foreach(MarketDataState.filtered_market_data, market_data_row)
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )
