import reflex as rx
from app.states.watchlist_state import WatchlistState, WatchedStock


def stock_card(stock: WatchedStock) -> rx.Component:
    is_gain = stock["change"] >= 0
    color_class = rx.cond(is_gain, "text-emerald-600", "text-red-600")
    bg_class = rx.cond(is_gain, "bg-emerald-50", "bg-red-50")
    border_color = rx.cond(
        is_gain, "group-hover:border-emerald-200", "group-hover:border-red-200"
    )
    icon_name = rx.cond(is_gain, "trending-up", "trending-down")
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h4(
                        stock["symbol"],
                        class_name="text-xl font-bold text-gray-900 tracking-tight",
                    ),
                    rx.el.span(
                        stock["name"], class_name="text-xs text-gray-500 font-semibold"
                    ),
                    class_name="flex flex-col",
                ),
                rx.el.button(
                    rx.icon(
                        "bell-plus",
                        size=20,
                        class_name="text-gray-300 hover:text-indigo-600 transition-colors",
                    ),
                    on_click=lambda: WatchlistState.open_alert_modal(stock["symbol"]),
                    class_name="p-2 hover:bg-indigo-50 rounded-full transition-all duration-200",
                    title="Set Alert",
                ),
                class_name="flex justify-between items-start mb-6",
            ),
            rx.el.div(
                rx.el.span(
                    f"${stock['price']:.2f}",
                    class_name="text-3xl font-bold text-gray-900 tracking-tight",
                ),
                rx.el.div(
                    rx.icon(icon_name, size=16, class_name=color_class),
                    rx.el.span(
                        f"{stock['change_pct']}%",
                        class_name=f"text-sm font-bold {color_class} ml-1",
                    ),
                    class_name=f"flex items-center px-3 py-1.5 rounded-full {bg_class}",
                ),
                class_name="flex items-center justify-between mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "52W Range",
                        class_name="text-[10px] font-bold text-gray-400 uppercase tracking-wider",
                    ),
                    rx.el.span(
                        f"${stock['low_52']} - ${stock['high_52']}",
                        class_name="text-xs font-bold text-gray-700",
                    ),
                    class_name="flex justify-between items-center py-1.5 border-b border-gray-100 border-dashed",
                ),
                rx.el.div(
                    rx.el.span(
                        "Volume",
                        class_name="text-[10px] font-bold text-gray-400 uppercase tracking-wider",
                    ),
                    rx.el.span(
                        stock["volume"], class_name="text-xs font-bold text-gray-700"
                    ),
                    class_name="flex justify-between items-center py-1.5 border-b border-gray-100 border-dashed",
                ),
                rx.el.div(
                    rx.el.span(
                        "Mkt Cap",
                        class_name="text-[10px] font-bold text-gray-400 uppercase tracking-wider",
                    ),
                    rx.el.span(
                        stock["market_cap"],
                        class_name="text-xs font-bold text-gray-700",
                    ),
                    class_name="flex justify-between items-center py-1.5",
                ),
                class_name="bg-gray-50/50 rounded-xl p-4 mb-5 border border-gray-100",
            ),
            rx.el.button(
                "Remove",
                on_click=lambda: WatchlistState.remove_from_watchlist(stock),
                class_name="w-full py-2.5 text-xs font-bold text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-xl transition-all duration-200 opacity-0 group-hover:opacity-100 translate-y-2 group-hover:translate-y-0",
            ),
            class_name="flex flex-col",
        ),
        class_name=f"bg-white rounded-3xl p-6 border border-gray-100 shadow-sm hover:shadow-[0_20px_40px_rgb(0,0,0,0.06)] hover:-translate-y-1 transition-all duration-300 group {border_color}",
    )