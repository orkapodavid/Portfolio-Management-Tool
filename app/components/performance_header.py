import reflex as rx
from app.states.portfolio_dashboard_state import (
    PortfolioDashboardState,
    KPIMetric,
    TopMover,
)


def kpi_card(metric: KPIMetric) -> rx.Component:
    """A single KPI metric card."""
    return rx.el.div(
        rx.el.span(
            metric["label"],
            class_name="text-[10px] font-bold text-gray-500 uppercase tracking-wide truncate",
        ),
        rx.el.div(
            metric["value"],
            class_name=rx.cond(
                metric["is_positive"],
                "text-lg font-bold text-[#00AA00] tracking-tight",
                "text-lg font-bold text-[#DD0000] tracking-tight",
            ),
        ),
        class_name="flex flex-col bg-white p-3 rounded-md shadow-sm border border-gray-200 min-w-[140px] flex-1 lg:flex-none",
    )


def mover_row(item: TopMover) -> rx.Component:
    """Row for the top movers grid."""
    return rx.el.tr(
        rx.el.td(item["ticker"], class_name="py-1 pl-2 font-bold text-gray-900"),
        rx.el.td(item["name"], class_name="py-1 text-gray-500 truncate max-w-[60px]"),
        rx.el.td(item["value"], class_name="py-1 font-medium text-gray-800 text-right"),
        rx.el.td(
            item["change"],
            class_name=rx.cond(
                item["is_positive"],
                "py-1 pr-2 font-bold text-[#00AA00] text-right",
                "py-1 pr-2 font-bold text-[#DD0000] text-right",
            ),
        ),
        class_name="text-[10px] border-b border-gray-100 last:border-0 hover:bg-gray-50",
    )


def mini_grid(title: str, data: list[TopMover]) -> rx.Component:
    """A compact 4-column grid for Top Movers."""
    return rx.el.div(
        rx.el.h4(
            title,
            class_name="text-[11px] font-bold text-[#333333] mb-1 px-2 pt-2 pb-1 border-b border-gray-200 uppercase tracking-wider",
        ),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "Ticker",
                        class_name="pl-2 text-left font-semibold text-gray-400",
                    ),
                    rx.el.th(
                        "Name", class_name="text-left font-semibold text-gray-400"
                    ),
                    rx.el.th(
                        "Value", class_name="text-right font-semibold text-gray-400"
                    ),
                    rx.el.th(
                        "Chg", class_name="pr-2 text-right font-semibold text-gray-400"
                    ),
                ),
                class_name="text-[9px] bg-gray-50",
            ),
            rx.el.tbody(rx.foreach(data, mover_row)),
            class_name="w-full",
        ),
        class_name="bg-white rounded-md shadow-sm border border-gray-200 flex-1 min-w-[280px] overflow-hidden",
    )


def performance_header() -> rx.Component:
    """The persistent performance header (Region 2)."""
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.foreach(PortfolioDashboardState.kpi_metrics, kpi_card),
                class_name="flex flex-wrap gap-2 lg:flex-nowrap lg:w-auto w-full mb-4 lg:mb-0",
            ),
            rx.el.div(
                mini_grid(
                    "Top Movers (Ops PnL)", PortfolioDashboardState.top_movers_ops
                ),
                mini_grid(
                    "Top Movers (YTD PnL)", PortfolioDashboardState.top_movers_ytd
                ),
                mini_grid("$ Delta Leaders", PortfolioDashboardState.top_movers_delta),
                mini_grid("Price Movers", PortfolioDashboardState.top_movers_price),
                mini_grid("Volume Leaders", PortfolioDashboardState.top_movers_volume),
                class_name="flex gap-2 flex-1 overflow-x-auto pb-2 scrollbar-thin scrollbar-thumb-gray-300 scrollbar-track-transparent",
            ),
            class_name="flex flex-col xl:flex-row gap-4 w-full items-start",
        ),
        class_name="bg-[#F0F0F0] border-b border-[#CCCCCC] p-4 shrink-0 shadow-[0_2px_4px_rgba(0,0,0,0.02)] sticky top-0 z-30",
    )