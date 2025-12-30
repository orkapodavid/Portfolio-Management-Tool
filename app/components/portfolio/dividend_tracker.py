import reflex as rx
from app.states.portfolio.portfolio_state import PortfolioState, Dividend


def dividend_row(div: Dividend) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.span(div["date"], class_name="text-sm text-gray-500"),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    div["symbol"], class_name="text-sm font-semibold text-gray-900"
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    f"${div['amount']:,.2f}",
                    class_name="text-sm font-medium text-emerald-600",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    f"{div['yield_on_cost']}%",
                    class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        class_name="hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-0",
    )


def dividend_tracker() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Dividend Tracker", class_name="text-lg font-bold text-gray-900"),
            rx.el.div(
                rx.el.span("Total Yield: ", class_name="text-sm text-gray-500"),
                rx.el.span("2.4%", class_name="text-sm font-bold text-emerald-600"),
                class_name="bg-emerald-50 px-3 py-1 rounded-lg",
            ),
            class_name="flex items-center justify-between mb-6 px-6 pt-6",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Date",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Symbol",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Amount",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Yield on Cost",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        class_name="bg-gray-50/50",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        PortfolioState.selected_portfolio["dividends"], dividend_row
                    ),
                    class_name="bg-white",
                ),
                class_name="min-w-full divide-y divide-gray-200 table-auto",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden h-fit",
    )