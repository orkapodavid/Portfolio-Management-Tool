import reflex as rx
from app.states.dashboard.dashboard_state import DashboardState


def summary_card(
    title: str,
    value: str,
    subtext: str,
    trend: str,
    trend_positive: bool,
    color_scheme: str,
) -> rx.Component:
    """
    Ultra compact summary card (~28px height) with left-border accent.
    """
    accent_border = rx.cond(
        trend_positive,
        "border-l-[3px] border-[#00AA00]",
        "border-l-[3px] border-[#DD0000]",
    )
    trend_color = rx.cond(trend_positive, "text-[#00AA00]", "text-[#DD0000]")
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                title,
                class_name="text-[7px] font-black text-gray-400 uppercase tracking-[0.1em] truncate mr-2",
            ),
            rx.el.div(
                rx.el.span(
                    value,
                    class_name="text-[10px] font-black text-gray-800 tracking-tighter",
                ),
                rx.el.span(
                    trend, class_name=f"text-[8px] font-black {trend_color} ml-1.5"
                ),
                class_name="flex items-center",
            ),
            class_name="flex flex-row items-center justify-between w-full",
        ),
        class_name=f"bg-white {accent_border} rounded-none shadow-sm px-2 py-0 border-y border-r border-gray-200 flex items-center min-w-[160px] h-[28px] hover:bg-gray-50 transition-colors",
    )


def portfolio_summary() -> rx.Component:
    return rx.el.div(
        summary_card(
            "Total Value",
            f"${DashboardState.total_value:,.2f}",
            "vs last mo",
            "+5.2%",
            True,
            "indigo",
        ),
        summary_card(
            "Daily Change",
            f"${DashboardState.daily_change_value:,.2f}",
            "vs yest",
            f"{DashboardState.daily_change_value / DashboardState.total_value * 100:.2f}%",
            rx.cond(DashboardState.daily_change_value >= 0, True, False),
            "blue",
        ),
        summary_card(
            "Total G/L",
            f"${DashboardState.total_gain_loss:,.2f}",
            "all time",
            f"{DashboardState.total_gain_loss_pct:.2f}%",
            rx.cond(DashboardState.total_gain_loss >= 0, True, False),
            "emerald",
        ),
        class_name="flex items-center gap-2",
    )