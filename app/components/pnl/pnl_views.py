import reflex as rx
from app.states.dashboard.portfolio_dashboard_state import (
    PortfolioDashboardState,
    PnLChangeItem,
    PnLSummaryItem,
    PnLCurrencyItem,
)
from app.constants import POSITIVE_GREEN, NEGATIVE_RED, ROW_HIGHLIGHT


def pnl_full_table() -> rx.Component:
    """Reuses PnL Change view structure for Full view as a superset."""
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Trade Date", align="left"),
                    header_cell("Underlying", align="left"),
                    header_cell("Ticker", align="left"),
                    header_cell("PnL YTD"),
                    header_cell("PnL Chg 1D"),
                    header_cell("PnL Chg 1W"),
                    header_cell("PnL Chg 1M"),
                    header_cell("PnL Chg% 1D"),
                    header_cell("PnL Chg% 1W"),
                    header_cell("PnL Chg% 1M"),
                )
            ),
            rx.el.tbody(
                rx.foreach(PortfolioDashboardState.filtered_pnl_change, pnl_change_row)
            ),
            class_name="w-full min-w-[1400px] table-auto border-separate border-spacing-0",
        ),
        type="hover",
        scrollbars="both",
        class_name="flex-1 w-full bg-white contain-strict",
    )


def header_cell(
    text: str,
    column_key: str = "",
    align: str = "right",
    sortable: bool = True,
    width: str = "auto",
    tooltip: str = "",
) -> rx.Component:
    """Standardized header cell for PnL tables with sorting and tooltips."""
    align_class = rx.match(
        align, ("left", "text-left"), ("center", "text-center"), "text-right"
    )
    is_sorted = PortfolioDashboardState.sort_column == column_key
    return rx.el.th(
        rx.el.div(
            rx.el.div(
                rx.el.span(text),
                rx.cond(
                    tooltip != "",
                    rx.el.span(
                        rx.icon("info", size=10, class_name="ml-1 text-gray-400"),
                        title=tooltip,
                        class_name="cursor-help shrink-0",
                    ),
                ),
                class_name="flex items-center",
            ),
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
        class_name=f"px-3 py-3 {align_class} text-[10px] font-bold text-gray-700 uppercase tracking-widest border-b-2 border-gray-400 align-middle whitespace-nowrap h-[44px] bg-[#E5E7EB] sticky top-0 z-30 shadow-[0_2px_4px_rgba(0,0,0,0.1)]",
        width=width,
    )


def value_cell(
    value: str,
    is_positive: bool = None,
    align: str = "right",
    magnitude: str = "normal",
) -> rx.Component:
    if is_positive != None:
        color_class = rx.cond(
            is_positive, f"text-[{POSITIVE_GREEN}]", f"text-[{NEGATIVE_RED}]"
        )
        bg_class = rx.match(
            magnitude,
            ("high", rx.cond(is_positive, "bg-green-50", "bg-red-50")),
            ("medium", rx.cond(is_positive, "bg-green-50/50", "bg-red-50/50")),
            "bg-transparent",
        )
    else:
        is_negative = value.to_string().startswith("-") | value.to_string().startswith(
            "("
        )
        color_class = rx.cond(
            is_negative, f"text-[{NEGATIVE_RED}]", f"text-[{POSITIVE_GREEN}]"
        )
        bg_class = rx.match(
            magnitude,
            ("high", rx.cond(~is_negative, "bg-green-50", "bg-red-50")),
            ("medium", rx.cond(~is_negative, "bg-green-50/50", "bg-red-50/50")),
            "bg-transparent",
        )
    return rx.el.td(
        value,
        class_name=f"px-3 py-2 text-[10px] font-mono font-bold {color_class} {bg_class} text-{align} border-b border-gray-200 align-middle whitespace-nowrap",
    )


def text_cell(value: str, align: str = "left", bold: bool = False) -> rx.Component:
    """Standard text cell."""
    font_weight = rx.cond(bold, "font-black", "font-medium")
    return rx.el.td(
        value,
        class_name=f"px-3 py-2 text-[10px] {font_weight} text-gray-700 text-{align} border-b border-gray-200 align-middle whitespace-nowrap",
    )


def pnl_change_row(item: PnLChangeItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["trade_date"], align="left"),
        text_cell(item["underlying"], align="left", bold=True),
        text_cell(item["ticker"], align="left"),
        value_cell(item["pnl_ytd"], magnitude="high"),
        value_cell(item["pnl_chg_1d"], magnitude="medium"),
        value_cell(item["pnl_chg_1w"]),
        value_cell(item["pnl_chg_1m"]),
        value_cell(item["pnl_chg_pct_1d"]),
        value_cell(item["pnl_chg_pct_1w"]),
        value_cell(item["pnl_chg_pct_1m"]),
        on_click=lambda: PortfolioDashboardState.set_selected_row(item["id"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-blue-50 hover:shadow-sm h-[40px] transition-all duration-150 cursor-pointer",
    )


def pnl_change_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Trade Date", column_key="trade_date", align="left"),
                    header_cell("Underlying", column_key="underlying", align="left"),
                    header_cell("Ticker", column_key="ticker", align="left"),
                    header_cell("PnL YTD", column_key="pnl_ytd"),
                    header_cell("PnL Chg 1D", column_key="pnl_chg_1d"),
                    header_cell("PnL Chg 1W", column_key="pnl_chg_1w"),
                    header_cell("PnL Chg 1M", column_key="pnl_chg_1m"),
                    header_cell("PnL Chg% 1D", column_key="pnl_chg_pct_1d"),
                    header_cell("PnL Chg% 1W", column_key="pnl_chg_pct_1w"),
                    header_cell("PnL Chg% 1M", column_key="pnl_chg_pct_1m"),
                )
            ),
            rx.el.tbody(
                rx.foreach(PortfolioDashboardState.filtered_pnl_change, pnl_change_row)
            ),
            class_name="w-full min-w-[1400px] table-auto border-separate border-spacing-0",
        ),
        type="hover",
        scrollbars="both",
        class_name="flex-1 w-full bg-white contain-strict",
    )


def pnl_summary_row(item: PnLSummaryItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["trade_date"], align="left"),
        text_cell(item["underlying"], align="left", bold=True),
        text_cell(item["currency"], align="center"),
        value_cell(item["price"], is_positive=True),
        value_cell(item["price_t_1"], is_positive=True),
        value_cell(item["price_change"]),
        value_cell(item["fx_rate"], is_positive=True),
        value_cell(item["fx_rate_t_1"], is_positive=True),
        value_cell(item["fx_rate_change"]),
        value_cell(item["dtl"], is_positive=True),
        value_cell(item["last_volume"], is_positive=True),
        value_cell(item["adv_3m"], is_positive=True),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 h-[40px] transition-colors",
    )


def pnl_summary_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Trade Date", align="left"),
                    header_cell("Underlying", align="left"),
                    header_cell("Currency", align="center"),
                    header_cell("Price"),
                    header_cell("Price (T-1)"),
                    header_cell("Price Change"),
                    header_cell("FX Rate"),
                    header_cell("FX Rate (T-1)"),
                    header_cell("FX Rate Change"),
                    header_cell("DTL", tooltip="Days To Liquidation"),
                    header_cell("Last Volume"),
                    header_cell("ADV 3M", tooltip="Average Daily Volume (3 Month)"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_pnl_summary, pnl_summary_row
                )
            ),
            class_name="w-full min-w-[1200px] table-auto border-separate border-spacing-0",
        ),
        type="hover",
        scrollbars="both",
        class_name="flex-1 w-full bg-white contain-strict",
    )


def pnl_currency_row(item: PnLCurrencyItem) -> rx.Component:
    return rx.el.tr(
        text_cell(item["trade_date"], align="left"),
        text_cell(item["currency"], align="center", bold=True),
        value_cell(item["fx_rate"], is_positive=True),
        value_cell(item["fx_rate_t_1"], is_positive=True),
        value_cell(item["fx_rate_change"]),
        value_cell(item["ccy_exposure"]),
        value_cell(item["usd_exposure"]),
        value_cell(item["pos_ccy_expo"]),
        value_cell(item["ccy_hedged_pnl"]),
        value_cell(item["pos_ccy_pnl"]),
        value_cell(item["net_ccy"]),
        value_cell(item["pos_c_truncated"]),
        class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 h-[40px] transition-colors",
    )


def pnl_currency_table() -> rx.Component:
    return rx.scroll_area(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    header_cell("Trade Date", align="left"),
                    header_cell("Currency", align="center"),
                    header_cell("FX Rate"),
                    header_cell("FX Rate (T-1)"),
                    header_cell("FX Rate Change"),
                    header_cell("CCY Exposure"),
                    header_cell("USD Exposure"),
                    header_cell("POS CCY Expo"),
                    header_cell("CCY Hedged PnL"),
                    header_cell("POS CCY PnL"),
                    header_cell("Net CC"),
                    header_cell("POS C (truncated)"),
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    PortfolioDashboardState.filtered_pnl_currency, pnl_currency_row
                )
            ),
            class_name="w-full min-w-[1200px] table-auto border-separate border-spacing-0",
        ),
        type="hover",
        scrollbars="both",
        class_name="flex-1 w-full bg-white contain-strict",
    )