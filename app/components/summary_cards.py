import reflex as rx
from app.states.dashboard_state import DashboardState


def summary_card(
    title: str,
    value: str,
    subtext: str,
    trend: str,
    trend_positive: bool,
    icon: str,
    color_scheme: str,
) -> rx.Component:
    """
    color_scheme options: "indigo", "emerald", "blue"
    """
    bg_gradient = rx.match(
        color_scheme,
        ("indigo", "bg-gradient-to-br from-indigo-500 to-indigo-600 shadow-indigo-200"),
        (
            "emerald",
            "bg-gradient-to-br from-emerald-500 to-emerald-600 shadow-emerald-200",
        ),
        "bg-gradient-to-br from-blue-500 to-blue-600 shadow-blue-200",
    )
    trend_color = rx.cond(trend_positive, "text-emerald-600", "text-red-600")
    trend_bg = rx.cond(trend_positive, "bg-emerald-50", "bg-red-50")
    trend_icon = rx.cond(trend_positive, "trending-up", "trending-down")
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name="h-6 w-6 text-white"),
                class_name=f"p-3.5 rounded-2xl {bg_gradient} w-fit shadow-lg transform transition-transform group-hover:scale-110 duration-300",
            ),
            rx.el.button(
                rx.icon(
                    "funnel",
                    size=20,
                    class_name="text-gray-300 hover:text-gray-600 transition-colors",
                ),
                class_name="p-1 -mr-2",
            ),
            class_name="flex justify-between items-start mb-6",
        ),
        rx.el.div(
            rx.el.p(
                title,
                class_name="text-sm font-semibold text-gray-500 mb-2 tracking-wide uppercase text-[11px]",
            ),
            rx.el.h3(
                value, class_name="text-3xl font-bold text-gray-900 tracking-tight"
            ),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(trend_icon, size=16, class_name=trend_color),
                rx.el.span(trend, class_name=f"text-sm font-bold {trend_color} ml-1.5"),
                class_name=f"flex items-center px-2.5 py-1 rounded-full {trend_bg} border border-transparent group-hover:border-{color_scheme}-100 transition-colors",
            ),
            rx.el.span(subtext, class_name="text-xs text-gray-400 font-medium ml-3"),
            class_name="flex items-center",
        ),
        class_name="bg-white rounded-3xl p-6 border border-gray-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgb(0,0,0,0.06)] transition-all duration-300 hover:-translate-y-1 group relative overflow-hidden",
    )


def portfolio_summary() -> rx.Component:
    return rx.el.div(
        summary_card(
            "Total Portfolio Value",
            f"${DashboardState.total_value:,.2f}",
            "vs last month",
            "+5.2%",
            True,
            "wallet",
            "indigo",
        ),
        summary_card(
            "Daily Change",
            f"${DashboardState.daily_change_value:,.2f}",
            "since yesterday",
            f"{DashboardState.daily_change_value / DashboardState.total_value * 100:,.2f}%",
            rx.cond(DashboardState.daily_change_value >= 0, True, False),
            "activity",
            "blue",
        ),
        summary_card(
            "Total Gain/Loss",
            f"${DashboardState.total_gain_loss:,.2f}",
            "all time return",
            f"{DashboardState.total_gain_loss_pct:,.2f}%",
            rx.cond(DashboardState.total_gain_loss >= 0, True, False),
            "bar-chart-2",
            "emerald",
        ),
        class_name=rx.cond(
            DashboardState.is_loading,
            "grid grid-cols-1 md:grid-cols-3 gap-6 w-full opacity-50 transition-opacity duration-200 pointer-events-none",
            "grid grid-cols-1 md:grid-cols-3 gap-6 w-full transition-opacity duration-200",
        ),
    )