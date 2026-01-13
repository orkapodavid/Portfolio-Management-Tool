import reflex as rx
from app.states.instruments.instrument_state import InstrumentState
from app.states.instruments.types import (
    TickerDataItem,
    StockScreenerItem,
    SpecialTermItem,
    InstrumentDataItem,
    InstrumentTermItem,
)


def header_cell(text: str, align: str = "left", column_key: str = "") -> rx.Component:
    align_class = rx.match(
        align, ("right", "text-right"), ("center", "text-center"), "text-left"
    )
    sort_icon = rx.cond(
        InstrumentState.sort_column == column_key,
        rx.cond(
            InstrumentState.sort_direction == "asc",
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
            column_key, InstrumentState.toggle_sort(column_key), None
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


def ticker_data_row(item: TickerDataItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["ticker"], clickable=True),
        text_cell(item["currency"]),
        text_cell(item["fx_rate"]),
        text_cell(item["sector"], clickable=False),
        text_cell(item["company"]),
        text_cell(item["po_lead_manager"]),
        text_cell(item["fmat_cap"]),
        text_cell(item["smkt_cap"]),
        text_cell(item["chg_1d_pct"]),
        text_cell(item["dtl"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def ticker_data_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Ticker"),
                    header_cell("Currency"),
                    header_cell("FX Rate"),
                    header_cell("Sector"),
                    header_cell("Company"),
                    header_cell("PO Lead Manager"),
                    header_cell("FMat Cap"),
                    header_cell("SMkt Cap"),
                    header_cell("1D%"),
                    header_cell("DTL"),
                )
            ),
            rx.el.tbody(
                rx.foreach(InstrumentState.filtered_ticker_data, ticker_data_row)
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def screener_row(item: StockScreenerItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["otl"]),
        text_cell(item["mkt_cap_37_pct"]),
        text_cell(item["ticker"]),
        text_cell(item["company"]),
        text_cell(item["country"]),
        text_cell(item["industry"]),
        text_cell(item["last_price"]),
        text_cell(item["mkt_cap_loc"]),
        text_cell(item["mkt_cap_usd"]),
        text_cell(item["adv_3m"]),
        text_cell(item["locate_qty_mm"]),
        text_cell(item["locate_f"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def stock_screener_view() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.select(
                rx.el.option("Select Country", value=""),
                class_name="border rounded px-2 py-1 text-xs appearance-none",
            ),
            rx.el.select(
                rx.el.option("Select Sector", value=""),
                class_name="border rounded px-2 py-1 text-xs appearance-none",
            ),
            rx.el.select(
                rx.el.option("Recorder", value=""),
                class_name="border rounded px-2 py-1 text-xs appearance-none",
            ),
            rx.el.select(
                rx.el.option("Sort 1", value=""),
                class_name="border rounded px-2 py-1 text-xs appearance-none",
            ),
            rx.el.select(
                rx.el.option("Sort 2", value=""),
                class_name="border rounded px-2 py-1 text-xs appearance-none",
            ),
            rx.el.select(
                rx.el.option("ADC", value=""),
                class_name="border rounded px-2 py-1 text-xs appearance-none",
            ),
            class_name="flex gap-2 p-2 bg-gray-50 border-b border-gray-200",
        ),
        rx.scroll_area(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        header_cell("OTL"),
                        header_cell("37% Market Cap"),
                        header_cell("Ticker"),
                        header_cell("Company"),
                        header_cell("Country"),
                        header_cell("Industry"),
                        header_cell("Last Price"),
                        header_cell("Market Cap (MM LOC)"),
                        header_cell("Market Cap (MM USD)"),
                        header_cell("ADV 3M"),
                        header_cell("Locate Qty (MM)"),
                        header_cell("Locate F"),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(InstrumentState.filtered_stock_screener, screener_row)
                ),
                class_name="w-full table-auto border-separate border-spacing-0",
            ),
            class_name="flex-1 w-full bg-white",
        ),
        class_name="flex flex-col h-full w-full bg-white",
    )


def special_term_row(item: SpecialTermItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["deal_num"]),
        text_cell(item["ticker"]),
        text_cell(item["company_name"]),
        text_cell(item["sec_type"]),
        text_cell(item["pos_loc"]),
        text_cell(item["account"]),
        text_cell(item["effective_date"]),
        text_cell(item["position"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def special_term_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Deal Num"),
                    header_cell("Ticker"),
                    header_cell("Company Name"),
                    header_cell("Sec Type"),
                    header_cell("Position Location"),
                    header_cell("Account"),
                    header_cell("Effective Date"),
                    header_cell("Position"),
                )
            ),
            rx.el.tbody(
                rx.foreach(InstrumentState.filtered_special_terms, special_term_row)
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def instrument_data_row(item: InstrumentDataItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["deal_num"]),
        text_cell(item["detail_id"]),
        text_cell(item["underlying"]),
        text_cell(item["ticker"]),
        text_cell(item["company_name"]),
        text_cell(item["sec_id"]),
        text_cell(item["sec_type"]),
        text_cell(item["pos_loc"]),
        text_cell(item["account"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def instrument_data_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Deal Num"),
                    header_cell("Detail ID"),
                    header_cell("Underlying"),
                    header_cell("Ticker"),
                    header_cell("Company Name"),
                    header_cell("SecID"),
                    header_cell("Sec Type"),
                    header_cell("Position Location"),
                    header_cell("Account"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    InstrumentState.filtered_instrument_data,
                    instrument_data_row,
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def instrument_term_row(item: InstrumentTermItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["deal_num"]),
        text_cell(item["detail_id"]),
        text_cell(item["underlying"]),
        text_cell(item["ticker"]),
        text_cell(item["company_name"]),
        text_cell(item["sec_type"]),
        text_cell(item["effective_date"]),
        text_cell(item["maturity_date"]),
        text_cell(item["first_reset_da"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def instrument_term_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Deal Num"),
                    header_cell("Detail ID"),
                    header_cell("Underlying"),
                    header_cell("Ticker"),
                    header_cell("Company Name"),
                    header_cell("Sec Type"),
                    header_cell("Effective Date"),
                    header_cell("Maturity Date"),
                    header_cell("First Reset Da (truncated)"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    InstrumentState.filtered_instrument_terms,
                    instrument_term_row,
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )
