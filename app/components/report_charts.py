import reflex as rx
from app.states.reports_state import ReportsState, AllocationMetric


def performance_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Portfolio vs Benchmark (S&P 500)",
                class_name="text-xl font-bold text-gray-900 tracking-tight",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        class_name="w-3 h-3 rounded-full bg-indigo-600 mr-2 ring-2 ring-white shadow-sm"
                    ),
                    rx.el.span(
                        "Portfolio",
                        class_name="text-xs font-bold text-gray-600 uppercase tracking-wide",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.div(
                    rx.el.div(
                        class_name="w-3 h-3 rounded-full bg-gray-300 mr-2 ring-2 ring-white shadow-sm"
                    ),
                    rx.el.span(
                        "S&P 500",
                        class_name="text-xs font-bold text-gray-600 uppercase tracking-wide",
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex items-center gap-6",
            ),
            class_name="flex items-center justify-between mb-8",
        ),
        rx.el.div(
            rx.recharts.line_chart(
                rx.recharts.cartesian_grid(
                    horizontal=True,
                    vertical=False,
                    class_name="opacity-20",
                    stroke_dasharray="3 3",
                ),
                rx.recharts.line(
                    data_key="portfolio_value",
                    stroke="#6366f1",
                    stroke_width=3,
                    type_="monotone",
                    dot=False,
                    active_dot={
                        "r": 6,
                        "fill": "#6366f1",
                        "stroke": "#fff",
                        "strokeWidth": 3,
                    },
                ),
                rx.recharts.line(
                    data_key="benchmark_value",
                    stroke="#9ca3af",
                    stroke_width=2,
                    stroke_dasharray="5 5",
                    type_="monotone",
                    dot=False,
                ),
                rx.recharts.x_axis(data_key="date", hide=True),
                rx.recharts.y_axis(
                    hide=False,
                    axis_line=False,
                    tick_line=False,
                    tick_size=10,
                    tick_count=5,
                    domain=["auto", "auto"],
                    class_name="text-xs font-medium text-gray-400",
                ),
                rx.recharts.tooltip(
                    content_style={
                        "backgroundColor": "rgba(255, 255, 255, 0.95)",
                        "borderRadius": "12px",
                        "border": "none",
                        "boxShadow": "0 10px 25px -5px rgba(0, 0, 0, 0.1)",
                        "padding": "12px",
                    }
                ),
                data=ReportsState.performance_data,
                width="100%",
                height=320,
            ),
            class_name="w-full",
        ),
        class_name="bg-white p-8 rounded-3xl border border-gray-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)]",
    )


def allocation_row(item: AllocationMetric) -> rx.Component:
    diff_color = rx.cond(item["diff"] >= 0, "text-emerald-600", "text-red-600")
    diff_prefix = rx.cond(item["diff"] >= 0, "+", "")
    return rx.el.tr(
        rx.el.td(
            rx.el.span(item["sector"], class_name="font-bold text-gray-800 text-sm"),
            class_name="px-5 py-4",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    class_name="h-2.5 rounded-full bg-indigo-500",
                    width=f"{item['actual_pct']}%",
                ),
                rx.el.span(
                    f"{item['actual_pct']}%",
                    class_name="ml-3 text-xs font-bold text-gray-600",
                ),
                class_name="flex items-center",
            ),
            class_name="px-5 py-4 w-1/3",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    class_name="h-2.5 rounded-full bg-gray-200",
                    width=f"{item['target_pct']}%",
                ),
                rx.el.span(
                    f"{item['target_pct']}%",
                    class_name="ml-3 text-xs font-bold text-gray-600",
                ),
                class_name="flex items-center",
            ),
            class_name="px-5 py-4 w-1/3",
        ),
        rx.el.td(
            rx.el.span(
                f"{diff_prefix}{item['diff']}%",
                class_name=f"font-bold {diff_color} text-sm",
            ),
            class_name="px-5 py-4 text-right",
        ),
        class_name="border-b border-gray-50 last:border-0 hover:bg-gray-50/80 transition-colors",
    )


def allocation_report() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Sector Allocation Analysis",
            class_name="text-xl font-bold text-gray-900 mb-6 tracking-tight",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Sector",
                            class_name="px-5 py-3 text-left text-[11px] font-bold text-gray-400 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Actual",
                            class_name="px-5 py-3 text-left text-[11px] font-bold text-gray-400 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Target",
                            class_name="px-5 py-3 text-left text-[11px] font-bold text-gray-400 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Diff",
                            class_name="px-5 py-3 text-right text-[11px] font-bold text-gray-400 uppercase tracking-wider",
                        ),
                        class_name="bg-gray-50/50",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(ReportsState.allocation_analysis, allocation_row)
                ),
                class_name="w-full",
            ),
            class_name="overflow-x-auto rounded-2xl border border-gray-100",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("info", size=18, class_name="text-blue-600 mt-0.5 shrink-0"),
                rx.el.p(
                    "Recommendation: Consider rebalancing your portfolio to reduce exposure to Technology and increase Financials to match your target allocation.",
                    class_name="text-sm text-blue-800 font-medium ml-3 leading-relaxed",
                ),
                class_name="flex items-start",
            ),
            class_name="mt-6 bg-blue-50/80 p-5 rounded-2xl border border-blue-100/50",
        ),
        class_name="bg-white p-8 rounded-3xl border border-gray-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)]",
    )


def metric_card(label: str, value: str, sublabel: str) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            label,
            class_name="text-[11px] text-gray-500 uppercase tracking-wider font-bold mb-2",
        ),
        rx.el.p(
            value, class_name="text-3xl font-bold text-gray-900 mb-2 tracking-tight"
        ),
        rx.el.p(sublabel, class_name="text-xs font-medium text-gray-400"),
        class_name="bg-gray-50/50 p-6 rounded-2xl border border-gray-100 hover:bg-white hover:shadow-lg transition-all duration-300 group",
    )


def summary_stats() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Key Performance Metrics",
            class_name="text-xl font-bold text-gray-900 mb-6 tracking-tight",
        ),
        rx.el.div(
            metric_card(
                "Total Return", f"{ReportsState.total_return_pct}%", "Annualized"
            ),
            metric_card(
                "Sharpe Ratio", f"{ReportsState.sharpe_ratio}", "Risk Adjusted"
            ),
            metric_card(
                "Max Drawdown", f"{ReportsState.max_drawdown}%", "Peak to Trough"
            ),
            metric_card("Alpha", f"{ReportsState.alpha}", "Excess Return"),
            class_name="grid grid-cols-2 lg:grid-cols-4 gap-6",
        ),
        class_name="bg-white p-8 rounded-3xl border border-gray-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] mb-8",
    )