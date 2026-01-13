import reflex as rx
from app.states.market_data.market_data_state import MarketDataState
from app.states.market_data.types import (
    MarketDataItem,
    FXDataItem,
    HistoricalDataItem,
    TradingCalendarItem,
    MarketHoursItem,
)


def header_cell(text: str, align: str = "left", column_key: str = "") -> rx.Component:
    align_class = rx.match(
        align, ("right", "text-right"), ("center", "text-center"), "text-left"
    )
    sort_icon = rx.cond(
        MarketDataState.sort_column == column_key,
        rx.cond(
            MarketDataState.sort_direction == "asc",
            rx.icon("arrow-up", size=10, class_name="ml-1 text-blue-600"),
            rx.icon("arrow-down", size=10, class_name="ml-1 text-blue-600"),
        ),
        rx.icon(
            "arrow-up-down",
            size=10,
            class_name="ml-1 text-gray-300 opacity-0 group-hover:opacity-100 transition-opacity",
        ),
    )
    return rx.el.th(
        rx.el.div(
            text,
            rx.cond(column_key != "", sort_icon, rx.fragment()),
            class_name=f"flex items-center {rx.match(align, ('right', 'justify-end'), ('center', 'justify-center'), 'justify-start')}",
        ),
        on_click=lambda: rx.cond(
            column_key, MarketDataState.toggle_sort(column_key), None
        ),
        class_name=f"px-3 py-3 {align_class} text-[10px] font-bold text-gray-700 uppercase tracking-widest border-b-2 border-gray-400 bg-[#E5E7EB] sticky top-0 z-30 shadow-sm h-[44px] whitespace-nowrap cursor-pointer hover:bg-gray-200 transition-colors group select-none",
    )


def text_cell(
    val: str, align: str = "left", bold: bool = False, clickable: bool = False
) -> rx.Component:
    base_class = f"px-3 py-2 text-[10px] text-gray-700 text-{align} border-b border-gray-200 align-middle whitespace-nowrap"
    if clickable:
        return rx.el.td(
            rx.el.a(val, class_name="text-blue-600 hover:underline cursor-pointer"),
            class_name=base_class,
        )
    weight = rx.cond(bold, "font-black", "font-medium")
    return rx.el.td(val, class_name=f"{base_class} {weight}")


def market_data_row(item: MarketDataItem) -> rx.Component:
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


def fx_data_row(item: FXDataItem) -> rx.Component:
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


def historical_row(item: HistoricalDataItem) -> rx.Component:
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


def calendar_row(item: TradingCalendarItem) -> rx.Component:
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


def hours_row(item: MarketHoursItem) -> rx.Component:
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
