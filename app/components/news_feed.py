import reflex as rx
from app.states.watchlist_state import WatchlistState, NewsItem


def news_card(item: NewsItem) -> rx.Component:
    sentiment_color = rx.match(
        item["sentiment"],
        ("Positive", "bg-emerald-50 text-emerald-700 border border-emerald-100"),
        ("Negative", "bg-red-50 text-red-700 border border-red-100"),
        "bg-gray-50 text-gray-700 border border-gray-100",
    )
    return rx.el.a(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        item["source"],
                        class_name="text-[11px] font-bold text-indigo-600 uppercase tracking-wide",
                    ),
                    rx.el.span("•", class_name="text-gray-300 mx-2"),
                    rx.el.span(
                        item["time_ago"],
                        class_name="text-[11px] font-medium text-gray-400",
                    ),
                    class_name="flex items-center mb-3",
                ),
                rx.el.h4(
                    item["headline"],
                    class_name="text-base font-bold text-gray-900 mb-3 leading-snug group-hover:text-indigo-600 transition-colors",
                ),
                rx.el.p(
                    item["summary"],
                    class_name="text-sm text-gray-500 line-clamp-2 leading-relaxed font-medium",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.foreach(
                        item["related_symbols"],
                        lambda s: rx.el.span(
                            s,
                            class_name="text-[10px] font-bold bg-gray-50 text-gray-600 px-2 py-1 rounded-lg border border-gray-100",
                        ),
                    ),
                    class_name="flex flex-wrap gap-2 mt-4",
                ),
                rx.el.span(
                    item["sentiment"],
                    class_name=f"text-[10px] font-bold px-2.5 py-1 rounded-full {sentiment_color} mt-4 self-start",
                ),
                class_name="flex items-center justify-between",
            ),
            class_name="flex flex-col h-full justify-between",
        ),
        href="#",
        class_name="block bg-white p-6 rounded-3xl border border-gray-100 shadow-[0_4px_20px_rgb(0,0,0,0.02)] hover:shadow-[0_10px_30px_rgb(0,0,0,0.06)] hover:-translate-y-1 transition-all duration-300 group",
    )


def news_feed() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                "Market News",
                class_name="text-xl font-bold text-gray-900 tracking-tight",
            ),
            rx.el.button(
                "View All",
                class_name="text-sm font-semibold text-indigo-600 hover:text-indigo-700 bg-indigo-50 hover:bg-indigo-100 px-3 py-1.5 rounded-lg transition-all",
            ),
            class_name="flex items-center justify-between mb-8",
        ),
        rx.el.div(
            rx.foreach(WatchlistState.news_feed, news_card),
            class_name="flex flex-col gap-5",
        ),
        class_name="bg-transparent",
    )