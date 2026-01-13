import reflex as rx
from app.states.events.events_state import EventsState
from app.states.types import (
    EventCalendarItem,
    EventStreamItem,
    ReverseInquiryItem,
)


def header_cell(text: str, align: str = "left", column_key: str = "") -> rx.Component:
    align_class = rx.match(
        align, ("right", "text-right"), ("center", "text-center"), "text-left"
    )
    sort_icon = rx.cond(
        EventsState.sort_column == column_key,
        rx.cond(
            EventsState.sort_direction == "asc",
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
        on_click=lambda: rx.cond(column_key, EventsState.toggle_sort(column_key), None),
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


def event_calendar_view() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Underlying", column_key="underlying"),
                    header_cell("Ticker", column_key="ticker"),
                    header_cell("Company", column_key="company"),
                    header_cell("Event Date", column_key="event_date"),
                    header_cell("Day Of Week", column_key="day_of_week"),
                    header_cell("Event Type", column_key="event_type"),
                    header_cell("Time", column_key="time"),
                )
            ),
            rx.el.tbody(rx.foreach(EventsState.filtered_event_calendar, event_cal_row)),
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
                        header_cell("Symbol", column_key="symbol"),
                        header_cell("Record Date"),
                        header_cell("Event Date"),
                        header_cell("Day of Week"),
                        header_cell("Event Type", column_key="event_type"),
                        header_cell("Subject", column_key="subject"),
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
                    rx.foreach(EventsState.filtered_event_stream, event_stream_row)
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


def reverse_inquiry_view() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Ticker", column_key="ticker"),
                    header_cell("Company", column_key="company"),
                    header_cell("Inquiry Date"),
                    header_cell("Expiry Date"),
                    header_cell("Deal Point"),
                    header_cell("Agent", column_key="agent"),
                    header_cell("Notes"),
                )
            ),
            rx.el.tbody(
                rx.foreach(EventsState.filtered_reverse_inquiry, reverse_inq_row)
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )
