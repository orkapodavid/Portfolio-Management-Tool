import reflex as rx
from app.states.dashboard_state import DashboardState, Holding


def performer_item(holding: Holding, is_gain: bool = True) -> rx.Component:
    bg_color = rx.cond(is_gain, "bg-emerald-50", "bg-red-50")
    text_color = rx.cond(is_gain, "text-emerald-600", "text-red-600")
    icon_name = rx.cond(is_gain, "trending-up", "trending-down")
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    holding["symbol"],
                    class_name="font-bold text-gray-900 text-sm group-hover:text-indigo-600 transition-colors",
                ),
                rx.el.p(
                    holding["name"],
                    class_name="text-xs text-gray-500 truncate max-w-[140px] font-medium",
                ),
                class_name="flex flex-col",
            ),
            class_name="flex items-center gap-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(icon_name, size=14, class_name=text_color),
                rx.el.span(
                    rx.cond(holding["daily_change_pct"] > 0, "+", ""),
                    f"{holding['daily_change_pct']}%",
                    class_name=f"text-xs font-bold {text_color} ml-1",
                ),
                class_name=f"flex items-center px-2.5 py-1 rounded-full {bg_color} border border-opacity-50 border-{rx.cond(is_gain, 'emerald', 'red')}-100",
            ),
            class_name="flex items-center",
        ),
        class_name="flex items-center justify-between py-4 border-b border-gray-50 last:border-0 hover:bg-gray-50 px-2 -mx-2 rounded-xl transition-all duration-200 group",
    )


def performers_widget() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("trophy", size=18, class_name="text-amber-500 mr-2"),
                rx.el.h3(
                    "Top Performers",
                    class_name="text-sm font-bold text-gray-900 uppercase tracking-wide",
                ),
                class_name="flex items-center mb-5",
            ),
            rx.el.div(
                rx.foreach(
                    DashboardState.top_performers,
                    lambda h: performer_item(h, is_gain=True),
                ),
                class_name="flex flex-col",
            ),
            class_name="bg-white rounded-3xl p-6 border border-gray-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] flex-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("trending-down", size=18, class_name="text-red-500 mr-2"),
                rx.el.h3(
                    "Top Losers",
                    class_name="text-sm font-bold text-gray-900 uppercase tracking-wide",
                ),
                class_name="flex items-center mb-5",
            ),
            rx.el.div(
                rx.foreach(
                    DashboardState.bottom_performers,
                    lambda h: performer_item(h, is_gain=False),
                ),
                class_name="flex flex-col",
            ),
            class_name="bg-white rounded-3xl p-6 border border-gray-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] flex-1",
        ),
        class_name="flex flex-col gap-6 h-full",
    )