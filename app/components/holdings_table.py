import reflex as rx
from app.states.dashboard_state import DashboardState, Holding


def status_badge(pct_change: float) -> rx.Component:
    return rx.el.span(
        rx.cond(pct_change >= 0, "+", ""),
        f"{pct_change}%",
        class_name=rx.cond(
            pct_change >= 0,
            "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800",
            "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800",
        ),
    )


def holding_row(holding: Holding) -> rx.Component:
    current_value = holding["shares"] * holding["current_price"]
    gain_loss = current_value - holding["shares"] * holding["avg_cost"]
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        holding["symbol"], class_name="font-semibold text-gray-900"
                    ),
                    rx.el.p(holding["name"], class_name="text-xs text-gray-500"),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(f"{holding['shares']}", class_name="text-sm text-gray-900"),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    f"${holding['current_price']:.2f}",
                    class_name="text-sm font-medium text-gray-900",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    f"${current_value:,.2f}",
                    class_name="text-sm font-medium text-gray-900",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    f"${gain_loss:,.2f}",
                    class_name=rx.cond(
                        gain_loss >= 0,
                        "text-sm font-medium text-emerald-600",
                        "text-sm font-medium text-red-600",
                    ),
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            status_badge(holding["daily_change_pct"]),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        class_name="hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-0",
    )


def holdings_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3("Holdings", class_name="text-xl font-bold text-gray-900"),
                rx.el.p(
                    "Current portfolio assets",
                    class_name="text-sm text-gray-500 font-medium",
                ),
                class_name="flex flex-col gap-0.5",
            ),
            rx.el.button(
                "View All",
                class_name="text-sm font-semibold text-indigo-600 hover:text-indigo-700 bg-indigo-50 hover:bg-indigo-100 px-4 py-2 rounded-xl transition-all duration-200",
            ),
            class_name="flex items-center justify-between mb-8 px-8 pt-8",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Symbol",
                            class_name="pl-8 pr-6 py-4 text-left text-xs font-bold text-gray-400 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Shares",
                            class_name="px-6 py-4 text-left text-xs font-bold text-gray-400 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Price",
                            class_name="px-6 py-4 text-left text-xs font-bold text-gray-400 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Value",
                            class_name="px-6 py-4 text-left text-xs font-bold text-gray-400 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Gain/Loss",
                            class_name="px-6 py-4 text-left text-xs font-bold text-gray-400 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Change",
                            class_name="px-6 py-4 text-left text-xs font-bold text-gray-400 uppercase tracking-wider",
                        ),
                        class_name="border-b border-gray-100",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(DashboardState.holdings, holding_row),
                    class_name=rx.cond(
                        DashboardState.is_loading,
                        "bg-white opacity-50 transition-opacity duration-200",
                        "bg-white transition-opacity duration-200",
                    ),
                ),
                class_name="min-w-full table-auto",
            ),
            class_name="overflow-x-auto pb-4",
        ),
        class_name="bg-white rounded-3xl border border-gray-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] overflow-hidden",
    )


def holding_row(holding: Holding) -> rx.Component:
    current_value = holding["shares"] * holding["current_price"]
    gain_loss = current_value - holding["shares"] * holding["avg_cost"]
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        holding["symbol"],
                        class_name="font-bold text-gray-900 text-sm group-hover:text-indigo-600 transition-colors",
                    ),
                    rx.el.p(
                        holding["name"], class_name="text-xs text-gray-500 font-medium"
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-center",
            ),
            class_name="pl-8 pr-6 py-5 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    f"{holding['shares']}",
                    class_name="text-sm font-semibold text-gray-700",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-5 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    f"${holding['current_price']:.2f}",
                    class_name="text-sm font-medium text-gray-900",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-5 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    f"${current_value:,.2f}",
                    class_name="text-sm font-bold text-gray-900",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-5 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    f"${gain_loss:,.2f}",
                    class_name=rx.cond(
                        gain_loss >= 0,
                        "text-sm font-bold text-emerald-600",
                        "text-sm font-bold text-red-600",
                    ),
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-5 whitespace-nowrap",
        ),
        rx.el.td(
            status_badge(holding["daily_change_pct"]),
            class_name="px-6 py-5 whitespace-nowrap",
        ),
        class_name="hover:bg-gray-50/80 transition-all duration-200 border-b border-gray-50 last:border-0 group",
    )


def status_badge(pct_change: float) -> rx.Component:
    return rx.el.span(
        rx.cond(pct_change >= 0, "+", ""),
        f"{pct_change}%",
        class_name=rx.cond(
            pct_change >= 0,
            "inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-gradient-to-r from-emerald-50 to-emerald-100 text-emerald-700 border border-emerald-100 shadow-sm",
            "inline-flex items-center px-3 py-1 rounded-full text-xs font-bold bg-gradient-to-r from-red-50 to-red-100 text-red-700 border border-red-100 shadow-sm",
        ),
    )