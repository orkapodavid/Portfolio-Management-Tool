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
                on_click=PortfolioDashboardState.dismiss_notification(
                    notification["id"]
                ),
                class_name="text-gray-600 hover:text-gray-900 bg-white/30 rounded-full p-0.5",
            ),
            class_name="flex justify-between items-start mb-1.5",
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
            class_name="flex justify-between items-center mb-1.5",
        ),
        rx.el.p(
            notification["instruction"],
            class_name=f"text-[10px] {text_color} leading-snug opacity-90",
        ),
        class_name=f"{bg_color} p-2.5 rounded-lg border-l-4 {border_color} shadow-sm hover:shadow-md transition-all duration-200 animate-in slide-in-from-right fade-in",
    )


def notification_sidebar() -> rx.Component:
    """The right sidebar component for notifications (Region 4) with slide transition."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "NOTIFICATIONS",
                            class_name="text-[10px] font-bold text-gray-500 tracking-widest",
                        ),
                        rx.el.button(
                            rx.icon("circle_plus", size=12, class_name="text-gray-400"),
                            on_click=PortfolioDashboardState.add_simulated_notification,
                            title="Simulate Live Alert",
                            class_name="hover:text-indigo-600 transition-colors",
                        ),
                        class_name="flex items-center justify-between mb-2 px-3 pt-3",
                    ),
                    rx.scroll_area(
                        rx.el.div(
                            rx.foreach(
                                PortfolioDashboardState.notifications, alert_card
                            ),
                            class_name="flex flex-col gap-2 p-2",
                        ),
                        type="hover",
                        scrollbars="vertical",
                        class_name="flex-1 w-full",
                    ),
                    class_name="h-full w-full flex flex-col min-w-[220px]",
                ),
                class_name="h-full w-full overflow-hidden",
            ),
            class_name=rx.cond(
                PortfolioDashboardState.is_sidebar_open,
                "w-[220px] opacity-100 border-l border-gray-200",
                "w-0 opacity-0 border-l-0 pointer-events-none",
            )
            + " flex bg-[#F9F9F9] h-full shrink-0 flex-col relative z-40 overflow-hidden transition-all duration-300 ease-in-out",
        )
    )