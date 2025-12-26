import reflex as rx
from app.states.portfolio_state import PortfolioState, Transaction


def transaction_row(tx: Transaction) -> rx.Component:
    is_buy = tx["type"] == "Buy"
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.span(tx["date"], class_name="text-sm text-gray-500"),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.span(
                    tx["type"],
                    class_name=rx.cond(
                        is_buy,
                        "px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800",
                        "px-2.5 py-0.5 rounded-full text-xs font-medium bg-red-100 text-red-800",
                    ),
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(tx["symbol"], class_name="text-sm font-semibold text-gray-900"),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(f"{tx['shares']}", class_name="text-sm text-gray-900"),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(f"${tx['price']:.2f}", class_name="text-sm text-gray-900"),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    f"${tx['amount']:,.2f}",
                    class_name="text-sm font-medium text-gray-900",
                ),
                class_name="flex items-center",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        class_name="hover:bg-gray-50 transition-colors border-b border-gray-100 last:border-0",
    )


def transaction_history() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Transaction History", class_name="text-lg font-bold text-gray-900"
            ),
            rx.el.button(
                "Export CSV",
                class_name="text-sm font-medium text-indigo-600 hover:text-indigo-700 transition-colors",
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
                            "Type",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Symbol",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Shares",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Price",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Total Amount",
                            class_name="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        class_name="bg-gray-50/50",
                    )
                ),
                rx.el.tbody(
                    rx.foreach(
                        PortfolioState.selected_portfolio["transactions"],
                        transaction_row,
                    ),
                    class_name="bg-white",
                ),
                class_name="min-w-full divide-y divide-gray-200 table-auto",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden h-fit",
    )