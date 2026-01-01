import reflex as rx
from app.components.shared.sidebar import sidebar
from app.components.shared.mobile_nav import mobile_nav
from app.states.research.research_state import ResearchState
from app.components.portfolio.research_components import (
    stock_analysis_card,
    stock_detail_modal,
)


def research_page() -> rx.Component:
    return rx.el.div(
        sidebar(current_page="Research"),
        stock_detail_modal(),
        rx.el.main(
            mobile_nav(current_page="Research"),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "Market Research",
                            class_name="text-2xl font-bold text-gray-900",
                        ),
                        rx.el.p(
                            "Analyze stocks and discover new investment opportunities.",
                            class_name="text-gray-500 text-sm mt-1",
                        ),
                        class_name="flex flex-col",
                    ),
                    rx.el.div(
                        rx.icon(
                            "search",
                            size=20,
                            class_name="text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                        ),
                        rx.el.input(
                            placeholder="Search symbol (e.g. NFLX)...",
                            on_change=ResearchState.set_search_query.debounce(600),
                            class_name="pl-10 pr-4 py-2.5 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-100 focus:border-indigo-500 outline-none w-full md:w-80 text-sm transition-all shadow-sm",
                        ),
                        class_name="relative w-full md:w-auto",
                    ),
                    class_name="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8",
                ),
                rx.cond(
                    ResearchState.filtered_stocks.length() > 0,
                    rx.el.div(
                        rx.foreach(ResearchState.filtered_stocks, stock_analysis_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "search-x", size=48, class_name="text-gray-300 mb-4"
                            ),
                            rx.el.h3(
                                "No stocks found",
                                class_name="text-lg font-medium text-gray-900",
                            ),
                            rx.el.p(
                                "Try adjusting your search terms.",
                                class_name="text-gray-500 text-sm mt-1",
                            ),
                            class_name="flex flex-col items-center justify-center py-16 bg-white rounded-2xl border border-dashed border-gray-300",
                        )
                    ),
                ),
                class_name="max-w-7xl mx-auto",
            ),
            class_name="flex-1 bg-gray-50/50 h-screen overflow-y-auto p-4 md:p-8",
        ),
        class_name="flex w-full h-screen font-['Inter'] bg-white text-gray-900",
    )