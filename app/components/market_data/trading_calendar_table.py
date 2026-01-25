"""
Trading Calendar Table Component.

Displays trading calendar for different markets.
"""

import reflex as rx
from app.states.market_data.market_data_state import MarketDataState
from app.states.market_data.types import TradingCalendarItem
from app.components.market_data.table_components import header_cell, text_cell


def calendar_row(item: TradingCalendarItem) -> rx.Component:
    """Render a single trading calendar row."""
    return rx.el.tr(
        text_cell(item["trade_date"]),
        text_cell(item["day_of_week"]),
        text_cell(item["usa"]),
        text_cell(item["hkg"]),
        text_cell(item["jpn"]),
        text_cell(item["aus"]),
        text_cell(item["nzl"]),
        text_cell(item["kor"]),
        text_cell(item["chn"]),
        text_cell(item["twn"]),
        text_cell(item["ind"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def trading_calendar_table() -> rx.Component:
    """
    Trading Calendar table component.

    Displays:
    - Trade Date, Day of Week
    - Market open/close status for: USA, HKG, JPN, AUS, NZL, KOR, CHN, TWN, IND
    """
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Trade Date"),
                    header_cell("Day of Week"),
                    header_cell("USA"),
                    header_cell("HKG"),
                    header_cell("JPN"),
                    header_cell("AUS"),
                    header_cell("NZL"),
                    header_cell("KOR"),
                    header_cell("CHN"),
                    header_cell("TWN"),
                    header_cell("IND"),
                )
            ),
            rx.el.tbody(rx.foreach(MarketDataState.trading_calendar, calendar_row)),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )
