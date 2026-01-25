"""
Market Hours Table Component.

Displays market session hours and status.
"""

import reflex as rx
from app.states.market_data.market_data_state import MarketDataState
from app.states.market_data.types import MarketHoursItem
from app.components.market_data.table_components import header_cell, text_cell


def hours_row(item: MarketHoursItem) -> rx.Component:
    """Render a single market hours row."""
    return rx.el.tr(
        text_cell(item["market"]),
        text_cell(item["ticker"]),
        text_cell(item["session"]),
        text_cell(item["local_time"]),
        text_cell(item["session_period"]),
        text_cell(item["is_open"]),
        text_cell(item["timezone"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def market_hours_table() -> rx.Component:
    """
    Market Hours table component.

    Displays:
    - Market, Ticker, Session
    - Local Time, Session Period, Is Open, Timezone
    """
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Market"),
                    header_cell("Ticker"),
                    header_cell("Session"),
                    header_cell("Local Time"),
                    header_cell("Session Period"),
                    header_cell("Is Open?"),
                    header_cell("Timezone"),
                )
            ),
            rx.el.tbody(rx.foreach(MarketDataState.market_hours, hours_row)),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )
