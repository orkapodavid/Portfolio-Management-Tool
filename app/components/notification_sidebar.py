import reflex as rx
from app.states.portfolio_dashboard_state import (
    PortfolioDashboardState,
    NotificationItem,
)


def alert_card(notification: NotificationItem) -> rx.Component:
    """Renders a single notification card."""
    bg_color = rx.match(
        notification["type"],
        ("alert", "bg-[#FFC000]"),
        ("warning", "bg-amber-200"),
        ("info", "bg-blue-100"),
        "bg-gray-100",
    )
    border_color = rx.match(
        notification["type"],
        ("alert", "border-yellow-700"),
        ("warning", "border-amber-500"),
        ("info", "border-blue-500"),
        "border-gray-400",
    )
    text_color = rx.cond(
        notification["type"] == "info", "text-blue-900", "text-gray-900"
    )
    return rx.el.div(
        rx.el.div(
            rx.el.h4(
                notification["header"],
                class_name=f"text-sm font-bold {text_color} leading-tight",
            ),
            rx.el.button(
                rx.icon("x", size=14),
                on_click=lambda: PortfolioDashboardState.dismiss_notification(
                    notification["id"]
                ),
                class_name="text-gray-600 hover:text-gray-900 bg-white/30 rounded-full p-0.5",
            ),
            class_name="flex justify-between items-start mb-2",
        ),
        rx.el.div(
            rx.el.span(
                notification["ticker"],
                class_name="text-xs font-bold text-gray-800 bg-white/50 px-1.5 py-0.5 rounded border border-black/5",
            ),
            rx.el.span(
                notification["timestamp"],
                class_name="text-[10px] font-medium text-gray-700/80",
            ),
            class_name="flex justify-between items-center mb-2",
        ),
        rx.el.p(
            notification["instruction"],
            class_name=f"text-xs {text_color} leading-snug opacity-90",
        ),
        class_name=f"{bg_color} p-3 rounded-lg border-l-4 {border_color} shadow-sm hover:shadow-md transition-all duration-200 animate-in slide-in-from-right fade-in",
    )


def notification_sidebar() -> rx.Component:
    """The right sidebar component for notifications (Region 4)."""
    return rx.cond(
        PortfolioDashboardState.is_sidebar_open,
        rx.el.aside(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "NOTIFICATIONS",
                        class_name="text-xs font-bold text-gray-500 tracking-widest",
                    ),
                    rx.el.button(
                        rx.icon("circle_plus", size=14, class_name="text-gray-400"),
                        on_click=PortfolioDashboardState.add_simulated_notification,
                        title="Simulate Live Alert",
                        class_name="hover:text-indigo-600 transition-colors",
                    ),
                    class_name="flex items-center justify-between mb-4",
                ),
                rx.el.div(
                    rx.foreach(PortfolioDashboardState.notifications, alert_card),
                    class_name="flex flex-col gap-3",
                ),
                class_name="p-4 h-full overflow-y-auto scrollbar-thin scrollbar-thumb-gray-200",
            ),
            class_name="w-[250px] bg-white border-l border-gray-200 h-full shrink-0 flex flex-col transition-all duration-300",
        ),
    )