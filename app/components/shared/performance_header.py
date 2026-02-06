import reflex as rx
from app.states.ui.performance_header_state import PerformanceHeaderState
from app.states.types import KPIMetric, TopMover
from app.constants import (
    POSITIVE_GREEN,
    NEGATIVE_RED,
    KPI_HEIGHT,
    MOVERS_ROW_HEIGHT,
    MOVERS_EXPANDED_HEIGHT,
    NAV_HEIGHT,
    FINANCIAL_GREY,
    ICON_KPI_SIZE,
)


def kpi_card(metric: KPIMetric) -> rx.Component:
    """An ultra-compact KPI metric card with deep vertical shrinkage and trend sparkline."""
    accent_color = rx.cond(
        metric["is_positive"], f"border-[{POSITIVE_GREEN}]", f"border-[{NEGATIVE_RED}]"
    )
    text_color = rx.cond(
        metric["is_positive"], f"text-[{POSITIVE_GREEN}]", f"text-[{NEGATIVE_RED}]"
    )
    sparkline_color = rx.cond(metric["is_positive"], POSITIVE_GREEN, NEGATIVE_RED)
    value_display = metric["value"]
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    metric["label"],
                    class_name="text-[7px] font-black text-gray-400 uppercase tracking-[0.15em] truncate",
                ),
                rx.el.span(
                    value_display,
                    class_name=f"text-[10px] font-black {text_color} tracking-tighter",
                ),
                class_name="flex flex-col",
            ),
            rx.el.svg(
                rx.el.svg.polyline(
                    points=metric["trend_data"],
                    stroke=sparkline_color,
                    fill="none",
                    stroke_width="2",
                ),
                view_box="0 0 50 24",
                class_name="w-8 h-4 opacity-40 shrink-0 ml-auto",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        class_name=f"flex items-center bg-white px-2 h-[{KPI_HEIGHT}] rounded-none shadow-sm border-l-[3px] {accent_color} border-y border-r border-gray-200 min-w-[50%] md:min-w-[155px] flex-1 hover:bg-gray-50 transition-colors",
    )


def mover_row(item: TopMover) -> rx.Component:
    """Ultra-compact row for top movers."""
    return rx.el.tr(
        rx.el.td(
            item["ticker"],
            class_name="py-0 pl-2 font-black text-gray-900 truncate text-[8px]",
        ),
        rx.el.td(
            item["value"],
            class_name="py-0 font-bold text-gray-700 text-right truncate text-[8px]",
        ),
        rx.el.td(
            item["change"],
            class_name=rx.cond(
                item["is_positive"],
                f"py-0 pr-2 font-black text-[{POSITIVE_GREEN}] text-right truncate text-[8px]",
                f"py-0 pr-2 font-black text-[{NEGATIVE_RED}] text-right truncate text-[8px]",
            ),
        ),
        class_name=f"border-b border-gray-100 last:border-0 hover:bg-gray-100 transition-colors h-[{MOVERS_ROW_HEIGHT}]",
    )


def mini_grid(title: str, data: list[TopMover]) -> rx.Component:
    """A compact grid for Top Movers."""
    return rx.el.div(
        rx.el.h4(
            title,
            class_name="text-[8px] font-black text-[#333333] px-2 py-0.5 border-b border-gray-200 uppercase tracking-widest bg-gray-100/50",
        ),
        rx.el.table(
            rx.el.tbody(rx.foreach(data, mover_row)), class_name="w-full table-fixed"
        ),
        class_name="bg-white border border-gray-200 overflow-hidden w-full shadow-sm rounded-sm",
    )


# Portfolio Summary Card Component
def summary_card(
    title: str,
    value: str,
    subtext: str,
    trend: str,
    trend_positive: bool,
    color_scheme: str,
) -> rx.Component:
    """
    Ultra compact summary card (~28px height) with left-border accent.
    """
    accent_border = rx.cond(
        trend_positive,
        "border-l-[3px] border-[#00AA00]",
        "border-l-[3px] border-[#DD0000]",
    )
    trend_color = rx.cond(trend_positive, "text-[#00AA00]", "text-[#DD0000]")
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                title,
                class_name="text-[7px] font-black text-gray-400 uppercase tracking-[0.1em] truncate mr-2",
            ),
            rx.el.div(
                rx.el.span(
                    value,
                    class_name="text-[10px] font-black text-gray-800 tracking-tighter",
                ),
                rx.el.span(
                    trend, class_name=f"text-[8px] font-black {trend_color} ml-1.5"
                ),
                class_name="flex items-center",
            ),
            class_name="flex flex-row items-center justify-between w-full",
        ),
        class_name=f"bg-white {accent_border} rounded-none shadow-sm px-2 py-0 border-y border-r border-gray-200 flex items-center min-w-[160px] h-[28px] hover:bg-gray-50 transition-colors",
    )


def portfolio_summary() -> rx.Component:
    """Portfolio summary cards using PerformanceHeaderState."""
    return rx.el.div(
        summary_card(
            "Total Value",
            f"${PerformanceHeaderState.portfolio_total_value:,.2f}",
            "vs last mo",
            "+5.2%",
            True,
            "indigo",
        ),
        summary_card(
            "Daily Change",
            f"${PerformanceHeaderState.portfolio_daily_change_value:,.2f}",
            "vs yest",
            f"{PerformanceHeaderState.portfolio_daily_change_value / PerformanceHeaderState.portfolio_total_value * 100:.2f}%",
            rx.cond(PerformanceHeaderState.portfolio_daily_change_value >= 0, True, False),
            "blue",
        ),
        summary_card(
            "Total G/L",
            f"${PerformanceHeaderState.portfolio_total_gain_loss:,.2f}",
            "all time",
            f"{PerformanceHeaderState.portfolio_total_gain_loss_pct:.2f}%",
            rx.cond(PerformanceHeaderState.portfolio_total_gain_loss >= 0, True, False),
            "emerald",
        ),
        class_name="flex items-center gap-2",
    )


def performance_header() -> rx.Component:
    """Persistently visible ultra-compact header with collapsible grid."""
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.foreach(PerformanceHeaderState.kpi_metrics, kpi_card),
                    class_name="flex flex-wrap md:flex-nowrap gap-0 overflow-visible flex-1",
                ),
                portfolio_summary(),
                class_name="flex items-center gap-2 w-full px-2 py-0",
            ),
            rx.el.div(
                rx.el.button(
                    rx.el.div(
                        rx.el.span(
                            rx.cond(
                                PerformanceHeaderState.show_top_movers,
                                "Hide Top Movers",
                                "Show Top Movers",
                            ),
                            class_name="text-[6px] font-black uppercase tracking-[0.3em]",
                        ),
                        rx.icon(
                            rx.cond(
                                PerformanceHeaderState.show_top_movers,
                                "chevron-up",
                                "chevron-down",
                            ),
                            size=ICON_KPI_SIZE,
                        ),
                        class_name="flex items-center gap-1 text-gray-500",
                    ),
                    on_click=PerformanceHeaderState.toggle_top_movers,
                    class_name="w-full flex items-center justify-center py-0 bg-gray-100 border-y border-gray-200 hover:bg-gray-200 transition-colors h-[12px]",
                ),
                rx.cond(
                    PerformanceHeaderState.show_top_movers,
                    rx.el.div(
                        rx.el.div(
                            mini_grid("Ops PnL", PerformanceHeaderState.top_movers_ops),
                            mini_grid("YTD PnL", PerformanceHeaderState.top_movers_ytd),
                            mini_grid(
                                "Delta Leaders",
                                PerformanceHeaderState.top_movers_delta,
                            ),
                            mini_grid("Price Movers", PerformanceHeaderState.top_movers_price),
                            mini_grid(
                                "Volume Leaders",
                                PerformanceHeaderState.top_movers_volume,
                            ),
                            class_name="flex flex-col md:flex-row gap-1 w-full p-1 bg-gray-100/30 overflow-x-auto",
                        ),
                        class_name=f"block w-full bg-white border-b border-gray-300 animate-in fade-in slide-in-from-top-1 duration-300 ease-in-out shadow-inner overflow-hidden h-auto md:h-[{MOVERS_EXPANDED_HEIGHT}] overflow-y-auto",
                    ),
                ),
                class_name="w-full",
            ),
            class_name="flex flex-col w-full items-start justify-between",
        ),
        on_mount=PerformanceHeaderState.load_performance_data,
        class_name=f"bg-[{FINANCIAL_GREY}] shrink-0 shadow-sm border-b border-gray-300 sticky top-[{NAV_HEIGHT}] z-50 bg-opacity-100",
    )
