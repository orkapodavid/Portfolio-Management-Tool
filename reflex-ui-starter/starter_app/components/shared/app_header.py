"""
App Header — Generalized KPI header component.

Renders a compact KPI strip with sparklines, summary cards,
and collapsible key items grid. Replaces PMT's performance_header
with generic app metrics.
"""

import reflex as rx
from starter_app.states.ui.app_header_state import AppHeaderState
from starter_app.states.ui.types import KPIMetric, TopMover
from starter_app.constants import (
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
    """An ultra-compact KPI metric card with trend sparkline."""
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


def item_row(item: TopMover) -> rx.Component:
    """Ultra-compact row for key items."""
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
    """A compact grid for key items."""
    return rx.el.div(
        rx.el.h4(
            title,
            class_name="text-[8px] font-black text-[#333333] px-2 py-0.5 border-b border-gray-200 uppercase tracking-widest bg-gray-100/50",
        ),
        rx.el.table(
            rx.el.tbody(rx.foreach(data, item_row)), class_name="w-full table-fixed"
        ),
        class_name="bg-white border border-gray-200 overflow-hidden w-full shadow-sm rounded-sm",
    )


def summary_card(
    title: str,
    value: str,
    trend: str,
    trend_positive: bool,
) -> rx.Component:
    """Ultra compact summary card (~28px height) with left-border accent."""
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


def app_summary() -> rx.Component:
    """App summary cards using AppHeaderState."""
    return rx.el.div(
        summary_card(
            "Total Requests",
            f"{AppHeaderState.app_total_requests:,.0f}",
            "+5.2%",
            True,
        ),
        summary_card(
            "Daily Requests",
            f"{AppHeaderState.app_daily_requests:,.0f}",
            "+1.0%",
            True,
        ),
        summary_card(
            "Success Rate",
            f"{AppHeaderState.app_success_rate:.2f}%",
            "+0.05%",
            True,
        ),
        class_name="flex items-center gap-2",
    )


def app_header() -> rx.Component:
    """Persistently visible ultra-compact header with collapsible grid."""
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.foreach(AppHeaderState.kpi_metrics, kpi_card),
                    class_name="flex flex-wrap md:flex-nowrap gap-0 overflow-visible flex-1",
                ),
                app_summary(),
                class_name="flex items-center gap-2 w-full px-2 py-0",
            ),
            rx.el.div(
                rx.el.button(
                    rx.el.div(
                        rx.el.span(
                            rx.cond(
                                AppHeaderState.show_top_items,
                                "Hide Key Items",
                                "Show Key Items",
                            ),
                            class_name="text-[6px] font-black uppercase tracking-[0.3em]",
                        ),
                        rx.icon(
                            rx.cond(
                                AppHeaderState.show_top_items,
                                "chevron-up",
                                "chevron-down",
                            ),
                            size=ICON_KPI_SIZE,
                        ),
                        class_name="flex items-center gap-1 text-gray-500",
                    ),
                    on_click=AppHeaderState.toggle_top_items,
                    class_name="w-full flex items-center justify-center py-0 bg-gray-100 border-y border-gray-200 hover:bg-gray-200 transition-colors h-[12px]",
                ),
                rx.cond(
                    AppHeaderState.show_top_items,
                    rx.el.div(
                        rx.el.div(
                            mini_grid("Top Endpoints", AppHeaderState.top_items_a),
                            mini_grid("Trending Down", AppHeaderState.top_items_b),
                            class_name="flex flex-col md:flex-row gap-1 w-full p-1 bg-gray-100/30 overflow-x-auto",
                        ),
                        class_name=f"block w-full bg-white border-b border-gray-300 animate-in fade-in slide-in-from-top-1 duration-300 ease-in-out shadow-inner overflow-hidden h-auto md:h-[{MOVERS_EXPANDED_HEIGHT}] overflow-y-auto",
                    ),
                ),
                class_name="w-full",
            ),
            class_name="flex flex-col w-full items-start justify-between",
        ),
        on_mount=AppHeaderState.load_header_data,
        class_name=f"bg-[{FINANCIAL_GREY}] shrink-0 shadow-sm border-b border-gray-300 sticky top-[{NAV_HEIGHT}] z-50 bg-opacity-100",
    )
