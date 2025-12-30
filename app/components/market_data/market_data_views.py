import reflex as rx
from app.states.dashboard.portfolio_dashboard_state import (
    PortfolioDashboardState,
    MarketDataItem,
    FXDataItem,
    HistoricalDataItem,
    TradingCalendarItem,
    MarketHoursItem,
    EventCalendarItem,
    EventStreamItem,
    ReverseInquiryItem,
)


def header_cell(text: str, align: str = "left") -> rx.Component:
    return rx.el.th(
        text,
        class_name=f"px-3 py-3 text-{align} text-[10px] font-bold text-gray-700 uppercase tracking-widest border-b-2 border-gray-400 bg-[#E5E7EB] sticky top-0 z-30 shadow-sm h-[44px] whitespace-nowrap",
    )


def text_cell(val: str) -> rx.Component:
    return rx.el.td(
        val,
        class_name="px-3 py-2 text-[10px] font-medium text-gray-700 border-b border-gray-200 align-middle whitespace-nowrap",
    )


def market_data_row(item: MarketDataItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["ticker"]),
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
                    header_cell("Ticker"),
                    header_cell("Listed Shares (mm)"),
                    header_cell("Last Volume"),
                    header_cell("Last Price"),
                    header_cell("vWAP Price"),
                    header_cell("Bid"),
                    header_cell("Ask"),
                    header_cell("1D Change %"),
                    header_cell("Implied Vol %"),
                    header_cell("Market Status"),
                    header_cell("Created by"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_market_data, market_data_row
                )
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
            rx.el.tbody(
                rx.foreach(PortfolioDashboardState.filtered_fx_data, fx_data_row)
            ),
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
                rx.foreach(
                    PortfolioDashboardState.filtered_historical_data, historical_row
                )
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
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_trading_calendar, calendar_row
                )
            ),
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
            rx.el.tbody(
                rx.foreach(PortfolioDashboardState.filtered_market_hours, hours_row)
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def event_cal_row(item: EventCalendarItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["underlying"]),
        text_cell(item["ticker"]),
        text_cell(item["company"]),
        text_cell(item["event_date"]),
        text_cell(item["day_of_week"]),
        text_cell(item["event_type"]),
        text_cell(item["time"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def event_calendar_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Underlying"),
                    header_cell("Ticker"),
                    header_cell("Company"),
                    header_cell("Event Date"),
                    header_cell("Day Of Week"),
                    header_cell("Event Type"),
                    header_cell("Time"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_event_calendar, event_cal_row
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def event_stream_row(item: EventStreamItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["symbol"]),
        text_cell(item["record_date"]),
        text_cell(item["event_date"]),
        text_cell(item["day_of_week"]),
        text_cell(item["event_type"]),
        text_cell(item["subject"]),
        text_cell(item["notes"]),
        text_cell(item["alerted"]),
        text_cell(item["recur"]),
        text_cell(item["created_by"]),
        text_cell(item["created_time"]),
        text_cell(item["updated_by"]),
        text_cell(item["updated_time"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def event_stream_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.input(
                        placeholder="Record Date",
                        class_name="border rounded px-2 py-1 text-xs w-24 h-7 outline-none focus:border-blue-500",
                    ),
                    rx.el.input(
                        placeholder="Event Date",
                        class_name="border rounded px-2 py-1 text-xs w-24 h-7 outline-none focus:border-blue-500",
                    ),
                    rx.el.input(
                        placeholder="Subject",
                        class_name="border rounded px-2 py-1 text-xs flex-1 h-7 outline-none focus:border-blue-500",
                    ),
                    rx.el.input(
                        placeholder="Notes",
                        class_name="border rounded px-2 py-1 text-xs flex-1 h-7 outline-none focus:border-blue-500",
                    ),
                    rx.el.input(
                        placeholder="Symbol",
                        class_name="border rounded px-2 py-1 text-xs w-20 h-7 outline-none focus:border-blue-500",
                    ),
                    rx.el.input(
                        placeholder="Event Type",
                        class_name="border rounded px-2 py-1 text-xs w-24 h-7 outline-none focus:border-blue-500",
                    ),
                    class_name="flex gap-2 w-full",
                ),
                rx.el.div(
                    rx.el.input(
                        placeholder="Recur Freq:",
                        class_name="border rounded px-2 py-1 text-xs w-24 h-7 outline-none focus:border-blue-500",
                    ),
                    rx.el.input(
                        placeholder="On Month:",
                        class_name="border rounded px-2 py-1 text-xs w-20 h-7 outline-none focus:border-blue-500",
                    ),
                    rx.el.input(
                        placeholder="On Dec:",
                        class_name="border rounded px-2 py-1 text-xs w-20 h-7 outline-none focus:border-blue-500",
                    ),
                    rx.el.label(
                        rx.el.input(type="checkbox", class_name="mr-1.5 h-3 w-3"),
                        "Alert",
                        class_name="text-xs font-bold flex items-center text-gray-700",
                    ),
                    rx.el.button(
                        "Filter Event",
                        class_name="bg-blue-600 text-white px-3 py-1 rounded text-[10px] font-bold hover:bg-blue-700 transition-colors shadow-sm",
                    ),
                    rx.el.button(
                        "Upload Event",
                        class_name="bg-gray-600 text-white px-3 py-1 rounded text-[10px] font-bold hover:bg-gray-700 transition-colors shadow-sm",
                    ),
                    class_name="flex gap-2 items-center w-full",
                ),
                class_name="flex flex-col gap-2",
            ),
            class_name="flex flex-col gap-2 p-2 bg-gray-50 border-b border-gray-200",
        ),
        rx.scroll_area(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        header_cell("Symbol"),
                        header_cell("Record Date"),
                        header_cell("Event Date"),
                        header_cell("Day of Week"),
                        header_cell("Event Type"),
                        header_cell("Subject"),
                        header_cell("Notes"),
                        header_cell("Alerted?"),
                        header_cell("Recur?"),
                        header_cell("Created By"),
                        header_cell("Created Time"),
                        header_cell("Updated By"),
                        header_cell("Updated Time"),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        PortfolioDashboardState.filtered_event_stream, event_stream_row
                    )
                ),
                class_name="w-full table-auto border-separate border-spacing-0",
            ),
            class_name="flex-1 w-full bg-white",
        ),
        class_name="flex flex-col h-full w-full bg-white",
    )


def reverse_inq_row(item: ReverseInquiryItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["ticker"]),
        text_cell(item["company"]),
        text_cell(item["inquiry_date"]),
        text_cell(item["expiry_date"]),
        text_cell(item["deal_point"]),
        text_cell(item["agent"]),
        text_cell(item["notes"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def reverse_inquiry_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Ticker"),
                    header_cell("Company"),
                    header_cell("Inquiry Date"),
                    header_cell("Expiry Date"),
                    header_cell("Deal Point"),
                    header_cell("Agent"),
                    header_cell("Notes"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_reverse_inquiry, reverse_inq_row
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )