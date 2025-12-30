import reflex as rx
from app.states.portfolio.portfolio_state import PortfolioState


def add_portfolio_modal() -> rx.Component:
    return rx.cond(
        PortfolioState.is_add_portfolio_open,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-gray-900/60 backdrop-blur-sm transition-opacity z-[100]",
                on_click=PortfolioState.toggle_add_portfolio,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Create New Portfolio",
                        class_name="text-xl font-bold text-gray-900",
                    ),
                    rx.el.button(
                        rx.icon("x", size=20, class_name="text-gray-400"),
                        on_click=PortfolioState.toggle_add_portfolio,
                        class_name="p-2 hover:bg-gray-100 rounded-full transition-colors",
                    ),
                    class_name="flex items-center justify-between mb-8",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.label(
                            "Portfolio Name",
                            class_name="block text-sm font-bold text-gray-700 mb-2",
                        ),
                        rx.el.input(
                            name="name",
                            placeholder="e.g., Retirement Fund",
                            class_name="w-full px-5 py-3 rounded-xl border border-gray-200 bg-gray-50 focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all font-medium",
                            required=True,
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Description",
                            class_name="block text-sm font-bold text-gray-700 mb-2",
                        ),
                        rx.el.textarea(
                            name="description",
                            placeholder="Brief description of your strategy...",
                            class_name="w-full px-5 py-3 rounded-xl border border-gray-200 bg-gray-50 focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all h-32 resize-none font-medium",
                        ),
                        class_name="mb-8",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            on_click=PortfolioState.toggle_add_portfolio,
                            class_name="px-6 py-2.5 text-sm font-bold text-gray-600 hover:bg-gray-50 rounded-xl transition-colors",
                        ),
                        rx.el.button(
                            "Create Portfolio",
                            type="submit",
                            class_name="px-6 py-2.5 text-sm font-bold text-white bg-gradient-to-r from-indigo-600 to-violet-600 hover:shadow-lg hover:shadow-indigo-500/30 rounded-xl transition-all duration-200 transform hover:-translate-y-0.5",
                        ),
                        class_name="flex items-center justify-end gap-3",
                    ),
                    on_submit=PortfolioState.add_portfolio,
                    reset_on_submit=True,
                ),
                class_name="bg-white rounded-3xl shadow-2xl w-full max-w-md p-8 relative z-[101] animate-in fade-in zoom-in duration-300 scale-100",
            ),
            class_name="fixed inset-0 z-[100] flex items-center justify-center p-4",
        ),
    )


def add_transaction_modal() -> rx.Component:
    return rx.cond(
        PortfolioState.is_add_transaction_open,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-gray-900/60 backdrop-blur-sm transition-opacity z-[100]",
                on_click=PortfolioState.toggle_add_transaction,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Add Transaction", class_name="text-xl font-bold text-gray-900"
                    ),
                    rx.el.button(
                        rx.icon("x", size=20, class_name="text-gray-400"),
                        on_click=PortfolioState.toggle_add_transaction,
                        class_name="p-2 hover:bg-gray-100 rounded-full transition-colors",
                    ),
                    class_name="flex items-center justify-between mb-8",
                ),
                rx.el.div(
                    rx.el.button(
                        "Buy",
                        on_click=lambda: PortfolioState.set_transaction_type("Buy"),
                        class_name=rx.cond(
                            PortfolioState.transaction_type == "Buy",
                            "flex-1 py-2.5 text-sm font-bold bg-emerald-500 text-white rounded-xl shadow-lg shadow-emerald-200 transition-all transform scale-105",
                            "flex-1 py-2.5 text-sm font-bold text-gray-500 hover:bg-gray-100 rounded-xl transition-all",
                        ),
                    ),
                    rx.el.button(
                        "Sell",
                        on_click=lambda: PortfolioState.set_transaction_type("Sell"),
                        class_name=rx.cond(
                            PortfolioState.transaction_type == "Sell",
                            "flex-1 py-2.5 text-sm font-bold bg-red-500 text-white rounded-xl shadow-lg shadow-red-200 transition-all transform scale-105",
                            "flex-1 py-2.5 text-sm font-bold text-gray-500 hover:bg-gray-100 rounded-xl transition-all",
                        ),
                    ),
                    class_name="flex gap-2 p-1.5 bg-gray-50 rounded-2xl mb-8 border border-gray-100",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Symbol",
                                class_name="block text-sm font-bold text-gray-700 mb-2",
                            ),
                            rx.el.input(
                                name="symbol",
                                placeholder="AAPL",
                                class_name="w-full px-5 py-3 rounded-xl border border-gray-200 bg-gray-50 focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all uppercase font-semibold",
                                required=True,
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Date",
                                class_name="block text-sm font-bold text-gray-700 mb-2",
                            ),
                            rx.el.input(
                                name="date",
                                type="date",
                                class_name="w-full px-5 py-3 rounded-xl border border-gray-200 bg-gray-50 focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all font-medium",
                                required=True,
                            ),
                        ),
                        class_name="grid grid-cols-2 gap-5 mb-5",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Shares",
                                class_name="block text-sm font-bold text-gray-700 mb-2",
                            ),
                            rx.el.input(
                                name="shares",
                                type="number",
                                step="0.0001",
                                placeholder="0.0",
                                class_name="w-full px-5 py-3 rounded-xl border border-gray-200 bg-gray-50 focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all font-medium",
                                required=True,
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Price per Share",
                                class_name="block text-sm font-bold text-gray-700 mb-2",
                            ),
                            rx.el.input(
                                name="price",
                                type="number",
                                step="0.01",
                                placeholder="$0.00",
                                class_name="w-full px-5 py-3 rounded-xl border border-gray-200 bg-gray-50 focus:bg-white focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all font-medium",
                                required=True,
                            ),
                        ),
                        class_name="grid grid-cols-2 gap-5 mb-8",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            on_click=PortfolioState.toggle_add_transaction,
                            class_name="px-6 py-2.5 text-sm font-bold text-gray-600 hover:bg-gray-50 rounded-xl transition-colors",
                        ),
                        rx.el.button(
                            "Submit Transaction",
                            type="submit",
                            class_name="px-6 py-2.5 text-sm font-bold text-white bg-gradient-to-r from-indigo-600 to-violet-600 hover:shadow-lg hover:shadow-indigo-500/30 rounded-xl transition-all duration-200 transform hover:-translate-y-0.5",
                        ),
                        class_name="flex items-center justify-end gap-3",
                    ),
                    on_submit=PortfolioState.add_transaction,
                    reset_on_submit=True,
                ),
                class_name="bg-white rounded-3xl shadow-2xl w-full max-w-md p-8 relative z-[101] animate-in fade-in zoom-in duration-300 scale-100",
            ),
            class_name="fixed inset-0 z-[100] flex items-center justify-center p-4",
        ),
    )