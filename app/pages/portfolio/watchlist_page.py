import reflex as rx
from app.components.shared.sidebar import sidebar
from app.components.shared.mobile_nav import mobile_nav
from app.states.portfolio.watchlist_state import WatchlistState, WatchedStock
from app.components.portfolio.stock_card import stock_card
from app.components.portfolio.alerts_panel import alerts_panel
from app.components.portfolio.news_feed import news_feed


def search_result_item(stock: WatchedStock) -> rx.Component:
    return rx.el.button(
        rx.el.div(
            rx.el.p(stock["symbol"], class_name="font-bold text-gray-900 text-sm"),
            rx.el.p(stock["name"], class_name="text-xs text-gray-500"),
            class_name="flex flex-col items-start",
        ),
        rx.el.div(
            rx.el.span(
                f"${stock['price']}",
                class_name="text-sm font-medium text-gray-700 mr-3",
            ),
            rx.icon("circle_play", size=18, class_name="text-indigo-600"),
            class_name="flex items-center",
        ),
        on_click=lambda: WatchlistState.add_to_watchlist(stock),
        class_name="flex items-center justify-between w-full p-3 hover:bg-gray-50 border-b border-gray-100 last:border-0 transition-colors text-left",
    )


def watchlist_page() -> rx.Component:
    return rx.el.div(
        sidebar(current_page="Watchlist"),
        rx.el.main(
            mobile_nav(current_page="Watchlist"),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "Watchlist", class_name="text-2xl font-bold text-gray-900"
                        ),
                        rx.el.p(
                            "Track your favorite stocks and set price alerts.",
                            class_name="text-gray-500 text-sm mt-1",
                        ),
                        class_name="flex flex-col",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.icon("refresh-cw", size=16, class_name="text-gray-500"),
                            "Refresh Prices",
                            on_click=WatchlistState.refresh_watchlist,
                            class_name="flex items-center gap-2 px-3 py-2 bg-white border border-gray-200 rounded-xl text-sm font-semibold text-gray-700 hover:bg-gray-50 transition-colors mr-4",
                        ),
                        rx.el.div(
                            rx.icon(
                                "search",
                                size=18,
                                class_name="text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                            ),
                            rx.el.input(
                                placeholder="Search symbol (e.g. AMD)...",
                                on_change=WatchlistState.set_search_query.debounce(500),
                                class_name="pl-10 pr-4 py-2 bg-white border border-gray-200 rounded-xl focus:ring-2 focus:ring-indigo-100 focus:border-indigo-500 outline-none w-64 text-sm transition-all",
                                default_value=WatchlistState.search_query,
                            ),
                            rx.cond(
                                WatchlistState.is_searching,
                                rx.el.div(
                                    rx.cond(
                                        WatchlistState.search_results.length() > 0,
                                        rx.foreach(
                                            WatchlistState.search_results,
                                            search_result_item,
                                        ),
                                        rx.el.div(
                                            "Searching / No stock found",
                                            class_name="p-3 text-sm text-gray-500",
                                        ),
                                    ),
                                    class_name="absolute top-full mt-2 left-0 w-full bg-white rounded-xl shadow-xl border border-gray-100 overflow-hidden z-20",
                                ),
                            ),
                            class_name="relative",
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.cond(
                            WatchlistState.watchlist.length() > 0,
                            rx.el.div(
                                rx.foreach(WatchlistState.watchlist, stock_card),
                                class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "eye-off",
                                        size=48,
                                        class_name="text-gray-300 mb-4",
                                    ),
                                    rx.el.h3(
                                        "Your watchlist is empty",
                                        class_name="text-lg font-medium text-gray-900",
                                    ),
                                    rx.el.p(
                                        "Search for stocks above to add them here.",
                                        class_name="text-gray-500 text-sm mt-1",
                                    ),
                                    class_name="flex flex-col items-center justify-center py-12 bg-white rounded-2xl border border-dashed border-gray-300",
                                )
                            ),
                        ),
                        class_name="lg:col-span-3",
                    ),
                    rx.el.div(
                        alerts_panel(),
                        news_feed(),
                        class_name="flex flex-col gap-8 lg:col-span-1",
                    ),
                    class_name="grid grid-cols-1 lg:grid-cols-4 gap-8",
                ),
                class_name="max-w-7xl mx-auto",
            ),
            class_name="flex-1 bg-gray-50/50 h-screen overflow-y-auto p-4 md:p-8",
        ),
        class_name="flex w-full h-screen font-['Inter'] bg-white text-gray-900",
    )