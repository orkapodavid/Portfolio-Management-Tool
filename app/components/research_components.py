import reflex as rx
from app.states.research_state import ResearchState, StockData


def stock_analysis_card(stock: StockData) -> rx.Component:
    is_gain = stock["change_pct"] >= 0
    color_class = rx.cond(is_gain, "text-emerald-600", "text-red-600")
    bg_class = rx.cond(is_gain, "bg-emerald-50", "bg-red-50")
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    stock["symbol"],
                    class_name="text-xl font-bold text-gray-900 tracking-tight",
                ),
                rx.el.span(
                    stock["name"], class_name="text-xs text-gray-500 font-semibold"
                ),
                class_name="flex flex-col",
            ),
            rx.el.div(
                rx.el.span(
                    f"${stock['price']}", class_name="text-xl font-bold text-gray-900"
                ),
                rx.el.span(
                    f"{stock['change_pct']}%",
                    class_name=f"text-xs font-bold px-2.5 py-1 rounded-full {bg_class} {color_class} ml-3",
                ),
                class_name="flex items-center",
            ),
            class_name="flex justify-between items-start mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "P/E Ratio",
                    class_name="text-xs font-semibold text-gray-400 uppercase tracking-wide",
                ),
                rx.el.span(
                    f"{stock['pe_ratio']}", class_name="text-sm font-bold text-gray-900"
                ),
                class_name="flex justify-between items-center py-2 border-b border-gray-50 border-dashed",
            ),
            rx.el.div(
                rx.el.span(
                    "Market Cap",
                    class_name="text-xs font-semibold text-gray-400 uppercase tracking-wide",
                ),
                rx.el.span(
                    stock["market_cap"], class_name="text-sm font-bold text-gray-900"
                ),
                class_name="flex justify-between items-center py-2 border-b border-gray-50 border-dashed",
            ),
            rx.el.div(
                rx.el.span(
                    "52W Range",
                    class_name="text-xs font-semibold text-gray-400 uppercase tracking-wide",
                ),
                rx.el.span(
                    f"${stock['low_52']} - ${stock['high_52']}",
                    class_name="text-sm font-bold text-gray-900",
                ),
                class_name="flex justify-between items-center py-2 border-b border-gray-50 border-dashed",
            ),
            rx.el.div(
                rx.el.span(
                    "Volume",
                    class_name="text-xs font-semibold text-gray-400 uppercase tracking-wide",
                ),
                rx.el.span(
                    stock["volume"], class_name="text-sm font-bold text-gray-900"
                ),
                class_name="flex justify-between items-center py-2",
            ),
            class_name="flex flex-col gap-1 mb-6",
        ),
        rx.el.button(
            "Detailed Analysis",
            on_click=lambda: ResearchState.open_modal(stock),
            class_name="w-full py-3 text-sm font-bold text-indigo-600 bg-indigo-50 hover:bg-indigo-100 rounded-xl transition-all duration-200 group-hover:bg-indigo-600 group-hover:text-white",
        ),
        class_name="bg-white p-6 rounded-3xl border border-gray-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgb(0,0,0,0.08)] hover:-translate-y-1 transition-all duration-300 group",
    )


def stock_detail_modal() -> rx.Component:
    return rx.cond(
        ResearchState.is_modal_open,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-gray-900/60 backdrop-blur-sm transition-opacity z-50",
                on_click=ResearchState.close_modal,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h2(
                                ResearchState.selected_stock["name"],
                                class_name="text-3xl font-bold text-gray-900 tracking-tight",
                            ),
                            rx.el.div(
                                rx.el.span(
                                    ResearchState.selected_stock["symbol"],
                                    class_name="px-2.5 py-1 bg-gray-100 text-gray-700 text-xs font-bold rounded-lg mr-3",
                                ),
                                rx.el.span(
                                    ResearchState.selected_stock["sector"],
                                    class_name="text-sm font-medium text-indigo-600 bg-indigo-50 px-2.5 py-1 rounded-lg",
                                ),
                                class_name="flex items-center mt-2",
                            ),
                            class_name="flex flex-col",
                        ),
                        rx.el.button(
                            rx.icon("x", size=24, class_name="text-gray-400"),
                            on_click=ResearchState.close_modal,
                            class_name="p-2 hover:bg-gray-100 rounded-full transition-colors",
                        ),
                        class_name="flex justify-between items-start mb-8",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Price History (30 Days)",
                                class_name="text-sm font-bold text-gray-900 mb-4",
                            ),
                            rx.recharts.line_chart(
                                rx.recharts.line(
                                    data_key="price",
                                    stroke="#6366f1",
                                    stroke_width=3,
                                    type_="monotone",
                                    dot=False,
                                ),
                                rx.recharts.x_axis(data_key="date", hide=True),
                                rx.recharts.y_axis(domain=["auto", "auto"], hide=True),
                                rx.recharts.tooltip(
                                    content_style={
                                        "backgroundColor": "#fff",
                                        "borderRadius": "12px",
                                        "border": "none",
                                        "boxShadow": "0 10px 25px -5px rgba(0, 0, 0, 0.1)",
                                        "padding": "12px",
                                    }
                                ),
                                data=ResearchState.chart_data,
                                width="100%",
                                height=240,
                            ),
                            class_name="bg-gray-50/50 rounded-2xl p-6 mb-8 border border-gray-100",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.p(
                                    "EPS (TTM)",
                                    class_name="text-xs font-semibold text-gray-400 uppercase mb-1",
                                ),
                                rx.el.p(
                                    ResearchState.selected_stock["eps"],
                                    class_name="text-xl font-bold text-gray-900",
                                ),
                                class_name="bg-white border border-gray-100 p-4 rounded-2xl shadow-sm",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "P/E Ratio",
                                    class_name="text-xs font-semibold text-gray-400 uppercase mb-1",
                                ),
                                rx.el.p(
                                    ResearchState.selected_stock["pe_ratio"],
                                    class_name="text-xl font-bold text-gray-900",
                                ),
                                class_name="bg-white border border-gray-100 p-4 rounded-2xl shadow-sm",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "High 52W",
                                    class_name="text-xs font-semibold text-gray-400 uppercase mb-1",
                                ),
                                rx.el.p(
                                    f"${ResearchState.selected_stock['high_52']}",
                                    class_name="text-xl font-bold text-gray-900",
                                ),
                                class_name="bg-white border border-gray-100 p-4 rounded-2xl shadow-sm",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "Low 52W",
                                    class_name="text-xs font-semibold text-gray-400 uppercase mb-1",
                                ),
                                rx.el.p(
                                    f"${ResearchState.selected_stock['low_52']}",
                                    class_name="text-xl font-bold text-gray-900",
                                ),
                                class_name="bg-white border border-gray-100 p-4 rounded-2xl shadow-sm",
                            ),
                            class_name="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8",
                        ),
                        rx.el.div(
                            rx.el.h4(
                                "About",
                                class_name="text-sm font-bold text-gray-900 mb-3",
                            ),
                            rx.el.p(
                                ResearchState.selected_stock["description"],
                                class_name="text-sm text-gray-600 leading-relaxed",
                            ),
                            class_name="mb-8",
                        ),
                        class_name="flex flex-col",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Add to Watchlist",
                            on_click=ResearchState.add_to_watchlist,
                            class_name="flex-1 px-6 py-3 bg-white border border-gray-200 text-gray-700 font-bold rounded-xl hover:bg-gray-50 transition-colors",
                        ),
                        rx.el.button(
                            "Buy Stock",
                            class_name="flex-1 px-6 py-3 bg-gradient-to-r from-indigo-600 to-violet-600 text-white font-bold rounded-xl hover:shadow-lg hover:shadow-indigo-500/30 transition-all transform hover:-translate-y-0.5",
                        ),
                        class_name="flex gap-4 mt-auto",
                    ),
                ),
                class_name="bg-white rounded-3xl shadow-2xl w-full max-w-2xl p-8 relative z-50 animate-in fade-in zoom-in duration-300 max-h-[90vh] overflow-y-auto",
            ),
            class_name="fixed inset-0 z-50 flex items-center justify-center p-4",
        ),
    )