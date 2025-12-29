import reflex as rx
from app.components.sidebar import sidebar
from app.components.mobile_nav import mobile_nav
from app.components.portfolio_modals import add_portfolio_modal, add_transaction_modal
from app.components.holdings_table import holdings_table
from app.components.transaction_history import transaction_history
from app.components.dividend_tracker import dividend_tracker
from app.components.sector_breakdown import sector_breakdown
from app.states.portfolio_state import PortfolioState


def portfolio_header() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(
                PortfolioState.selected_portfolio["name"],
                class_name="text-2xl font-bold text-gray-900",
            ),
            rx.el.p(
                PortfolioState.selected_portfolio["description"],
                class_name="text-gray-500 text-sm mt-1",
            ),
            class_name="flex flex-col",
        ),
        rx.el.div(
            rx.el.select(
                rx.foreach(
                    PortfolioState.portfolios,
                    lambda p, i: rx.el.option(p["name"], value=i),
                ),
                on_change=lambda e: PortfolioState.set_portfolio_index(e),
                class_name="bg-white border border-gray-200 text-gray-700 text-sm rounded-xl focus:ring-indigo-500 focus:border-indigo-500 block px-4 py-2 appearance-none",
            ),
            rx.el.button(
                rx.icon("plus", size=16, class_name="mr-2"),
                "New Portfolio",
                on_click=PortfolioState.toggle_add_portfolio,
                class_name="flex items-center bg-white border border-gray-200 text-gray-700 px-4 py-2 rounded-xl text-sm font-semibold hover:bg-gray-50 transition-colors",
            ),
            rx.el.button(
                rx.icon("arrow-up-right", size=16, class_name="mr-2"),
                "Add Transaction",
                on_click=PortfolioState.toggle_add_transaction,
                class_name="flex items-center bg-indigo-600 text-white px-4 py-2 rounded-xl text-sm font-semibold hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-200",
            ),
            class_name="flex items-center gap-3",
        ),
        class_name="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8",
    )


def portfolio_page() -> rx.Component:
    return rx.el.div(
        sidebar(current_page="Portfolios"),
        add_portfolio_modal(),
        add_transaction_modal(),
        rx.el.main(
            mobile_nav(current_page="Portfolios"),
            rx.el.div(
                portfolio_header(),
                rx.el.div(
                    rx.el.div(
                        holdings_table(),
                        transaction_history(),
                        class_name="flex flex-col gap-6 lg:col-span-2",
                    ),
                    rx.el.div(
                        sector_breakdown(),
                        dividend_tracker(),
                        class_name="flex flex-col gap-6 lg:col-span-1",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-3 gap-6",
                ),
                class_name="max-w-7xl mx-auto",
            ),
            class_name="flex-1 bg-gray-50/50 h-screen overflow-y-auto p-4 md:p-8",
        ),
        class_name="flex w-full h-screen font-['Inter'] bg-white text-gray-900",
    )