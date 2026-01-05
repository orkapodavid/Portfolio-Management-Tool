import reflex as rx
from app.states.dashboard.portfolio_dashboard_state import (
    PortfolioDashboardState,
    PositionItem,
    StockPositionItem,
    WarrantPositionItem,
    BondPositionItem,
    TradeSummaryItem,
)
from app.constants import POSITIVE_GREEN, NEGATIVE_RED


def header_cell(
    text: str, column_key: str = "", align: str = "right", sortable: bool = True
) -> rx.Component:
    align_class = rx.match(
        align, ("left", "text-left"), ("center", "text-center"), "text-right"
    )
    is_sorted = PortfolioDashboardState.sort_column == column_key
    return rx.el.th(
        rx.el.div(
            rx.el.span(text),
            rx.cond(
                sortable,
                rx.cond(
                    is_sorted,
                    rx.icon(
                        rx.cond(
                            PortfolioDashboardState.sort_direction == "asc",
                            "arrow-up",
                            "arrow-down",
                        ),
                        size=10,
                        class_name="ml-1 text-blue-600",
                    ),
                    rx.icon(
                        "arrow-up-down",
                        size=10,
                        class_name="ml-1 text-gray-400 opacity-0 group-hover:opacity-100",
                    ),
                ),
            ),
            class_name=f"flex items-center {rx.match(align, ('left', 'justify-start'), ('center', 'justify-center'), 'justify-end')} group cursor-pointer",
            on_click=lambda: rx.cond(
                sortable, PortfolioDashboardState.toggle_sort(column_key), None
            ),
        ),
        class_name=f"px-3 py-3 {align_class} text-[10px] font-bold text-gray-700 uppercase tracking-widest border-b-2 border-gray-400 bg-[#E5E7EB] sticky top-0 z-30 shadow-[0_2px_4px_rgba(0,0,0,0.1)] h-[44px]",
    )


def value_cell(
    val: str, is_positive: bool = True, align: str = "right"
) -> rx.Component:
    color = rx.cond(is_positive, f"text-[{POSITIVE_GREEN}]", f"text-[{NEGATIVE_RED}]")
    return rx.el.td(
        val,
        class_name=f"px-3 py-2 text-[10px] font-mono font-bold {color} text-{align} border-b border-gray-200 align-middle",
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


def positions_row(p: PositionItem) -> rx.Component:
    return rx.el.tr(
        text_cell(p["trade_date"]),
        text_cell(p["deal_num"]),
        text_cell(p["detail_id"]),
        text_cell(p["underlying"]),
        text_cell(p["ticker"], bold=True),
        text_cell(p["company_name"]),
        text_cell(p["account_id"]),
        text_cell(p["pos_loc"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def positions_table() -> rx.Component:
    return rx.el.div(
        rx.scroll_area(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        header_cell("Trade Date", "left"),
                        header_cell("Deal Num", "left"),
                        header_cell("Detail ID", "left"),
                        header_cell("Underlying", "left"),
                        header_cell("Ticker", "left"),
                        header_cell("Company Name", "left"),
                        header_cell("Account ID", "left"),
                        header_cell("Pos Loc", "left"),
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        PortfolioDashboardState.filtered_positions, positions_row
                    )
                ),
                class_name="w-full table-auto border-separate border-spacing-0",
            ),
            class_name="flex-1 w-full bg-white",
        ),
        rx.el.div(
            rx.el.button(
                "Generate Positions",
                class_name="bg-blue-600 text-white text-xs font-bold py-2 px-4 rounded hover:bg-blue-700 transition-colors shadow-sm",
                on_click=lambda: PortfolioDashboardState.handle_generate("Positions"),
            ),
            class_name="p-3 border-t border-gray-200 bg-gray-50 flex justify-center",
        ),
        class_name="flex flex-col h-full w-full bg-white",
    )


def stock_position_row(p: StockPositionItem) -> rx.Component:
    return rx.el.tr(
        text_cell(p["trade_date"]),
        text_cell(p["deal_num"]),
        text_cell(p["detail_id"]),
        text_cell(p["ticker"], bold=True),
        text_cell(p["company_name"]),
        text_cell(p["sec_id"]),
        text_cell(p["sec_type"]),
        text_cell(p["currency"], align="center"),
        text_cell(p["account_id"]),
        text_cell(p["position_location"]),
        text_cell(p["notional"], align="right"),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def stock_position_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Trade Date", "left"),
                    header_cell("Deal Num", "left"),
                    header_cell("Detail ID", "left"),
                    header_cell("Ticker", "left"),
                    header_cell("Company Name", "left"),
                    header_cell("SecID", "left"),
                    header_cell("Sec Type", "left"),
                    header_cell("Currency", "center"),
                    header_cell("Account ID", "left"),
                    header_cell("Position Location", "left"),
                    header_cell("Notional", "right"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_stock_positions, stock_position_row
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def warrant_position_row(p: WarrantPositionItem) -> rx.Component:
    return rx.el.tr(
        text_cell(p["trade_date"]),
        text_cell(p["deal_num"]),
        text_cell(p["detail_id"]),
        text_cell(p["underlying"], bold=True),
        text_cell(p["ticker"]),
        text_cell(p["company_name"]),
        text_cell(p["sec_id"]),
        text_cell(p["sec_type"]),
        text_cell(p["subtype"]),
        text_cell(p["currency"], align="center"),
        text_cell(p["account_id"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def warrant_position_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Trade Date", "left"),
                    header_cell("Deal Num", "left"),
                    header_cell("Detail ID", "left"),
                    header_cell("Underlying", "left"),
                    header_cell("Ticker", "left"),
                    header_cell("Company Name", "left"),
                    header_cell("SecID", "left"),
                    header_cell("Sec Type", "left"),
                    header_cell("Subtype", "left"),
                    header_cell("Currency", "center"),
                    header_cell("Account ID", "left"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_warrant_positions,
                    warrant_position_row,
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def bond_position_row(p: BondPositionItem) -> rx.Component:
    return rx.el.tr(
        text_cell(p["trade_date"]),
        text_cell(p["deal_num"]),
        text_cell(p["detail_id"]),
        text_cell(p["underlying"], bold=True),
        text_cell(p["ticker"]),
        text_cell(p["company_name"]),
        text_cell(p["sec_id"]),
        text_cell(p["sec_type"]),
        text_cell(p["subtype"]),
        text_cell(p["currency"], align="center"),
        text_cell(p["account_id"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def bond_position_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Trade Date", "left"),
                    header_cell("Deal Num", "left"),
                    header_cell("Detail ID", "left"),
                    header_cell("Underlying", "left"),
                    header_cell("Ticker", "left"),
                    header_cell("Company Name", "left"),
                    header_cell("SecID", "left"),
                    header_cell("Sec Type", "left"),
                    header_cell("Subtype", "left"),
                    header_cell("Currency", "center"),
                    header_cell("Account ID", "left"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_bond_positions, bond_position_row
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )


def trade_summary_row(p: TradeSummaryItem) -> rx.Component:
    return rx.el.tr(
        text_cell(p["deal_num"]),
        text_cell(p["detail_id"]),
        text_cell(p["ticker"], bold=True),
        text_cell(p["underlying"]),
        text_cell(p["account_id"]),
        text_cell(p["company_name"]),
        text_cell(p["sec_id"]),
        text_cell(p["sec_type"]),
        text_cell(p["subtype"]),
        text_cell(p["currency"], align="center"),
        text_cell(p["closing_date"], align="center"),
        text_cell(p["divisor"], align="right"),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors h-[40px]",
    )


def trade_summary_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Deal Num", "left"),
                    header_cell("Detail ID", "left"),
                    header_cell("Ticker", "left"),
                    header_cell("Underlying", "left"),
                    header_cell("Account ID", "left"),
                    header_cell("Company Name", "left"),
                    header_cell("SecID", "left"),
                    header_cell("Sec Type", "left"),
                    header_cell("Subtype", "left"),
                    header_cell("Currency", "center"),
                    header_cell("Closing Date", "center"),
                    header_cell("Divisor", "right"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_trade_summaries, trade_summary_row
                )
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="flex-1 w-full bg-white",
    )