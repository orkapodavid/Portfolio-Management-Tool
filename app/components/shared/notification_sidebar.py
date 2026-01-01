import reflex as rx
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState
from app.states.dashboard.portfolio_dashboard_types import NotificationItem
from app.states.notifications.notification_pagination_state import (
    NotificationPaginationState,
)


def alert_card(notification: NotificationItem) -> rx.Component:
    """Renders a single notification card with standardized Amber styling."""
    from app.constants import ALERT_AMBER

    bg_color = rx.match(
        notification["type"],
        ("alert", f"bg-[{ALERT_AMBER}]"),
        ("warning", "bg-amber-200"),
        ("info", "bg-blue-100"),
        "bg-gray-100",
    )
    border_color = rx.match(
        notification["type"],
        ("alert", "border-black/20"),
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
                class_name=f"text-[11px] font-black {text_color} leading-tight uppercase tracking-wider",
            ),
            rx.el.button(
                rx.icon("circle-x", size=14),
                on_click=PortfolioDashboardState.dismiss_notification(
                    notification["id"]
                ),
                class_name="text-gray-900/60 hover:text-black transition-colors",
            ),
            class_name="flex justify-between items-start mb-2",
        ),
        rx.el.div(
            rx.el.span(
                notification["ticker"],
                class_name="text-[10px] font-black text-gray-900 bg-white/40 px-1.5 py-0.5 rounded border border-black/10",
            ),
            rx.el.span(
                notification["timestamp"],
                class_name="text-[9px] font-bold text-gray-800/60",
            ),
            class_name="flex justify-between items-center mb-2",
        ),
        rx.el.p(
            notification["instruction"],
            class_name=f"text-[10px] font-bold {text_color} leading-snug",
        ),
        class_name=f"{bg_color} p-3 rounded-md border-l-4 {border_color} shadow-sm hover:shadow-md transition-all duration-300 animate-in slide-in-from-right fade-in",
    )


def pagination_footer() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.el.div(
                rx.icon("chevron-left", size=12),
                rx.el.span("Prev", class_name="ml-1"),
                class_name="flex items-center",
            ),
            on_click=NotificationPaginationState.prev_page,
            disabled=NotificationPaginationState.current_page == 1,
            class_name="px-2 py-1 rounded hover:bg-gray-200 disabled:opacity-30 disabled:cursor-not-allowed transition-all text-[9px] font-black uppercase tracking-tighter",
        ),
        rx.el.span(
            f"{NotificationPaginationState.current_page} / {NotificationPaginationState.total_pages}",
            class_name="text-[10px] font-black text-gray-600 tabular-nums",
        ),
        rx.el.button(
            rx.el.div(
                rx.el.span("Next", class_name="mr-1"),
                rx.icon("chevron-right", size=12),
                class_name="flex items-center",
            ),
            on_click=NotificationPaginationState.next_page,
            disabled=NotificationPaginationState.current_page
            == NotificationPaginationState.total_pages,
            class_name="px-2 py-1 rounded hover:bg-gray-200 disabled:opacity-30 disabled:cursor-not-allowed transition-all text-[9px] font-black uppercase tracking-tighter",
        ),
        class_name="flex items-center justify-between px-3 py-2 border-t border-gray-200 bg-white/80 backdrop-blur-sm sticky bottom-0",
    )


def notification_sidebar() -> rx.Component:
    """The right sidebar component for notifications (Region 4) with slide transition and pagination."""
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "NOTIFICATIONS",
                                class_name="text-[10px] font-black text-gray-500 tracking-widest",
                            ),
                            rx.el.span(
                                PortfolioDashboardState.notifications.length().to_string(),
                                class_name="ml-2 bg-gray-200 text-gray-700 text-[8px] font-black px-1.5 py-0.5 rounded-full",
                            ),
                            class_name="flex items-center",
                        ),
                        rx.el.div(
                            rx.el.button(
                                rx.icon(
                                    "rotate-ccw", size=12, class_name="text-gray-400"
                                ),
                                on_click=NotificationPaginationState.reset_pagination,
                                title="Reset Page",
                                class_name="hover:text-blue-600 transition-colors mr-2",
                            ),
                            rx.el.button(
                                rx.icon(
                                    "circle_plus", size=12, class_name="text-gray-400"
                                ),
                                on_click=PortfolioDashboardState.add_simulated_notification,
                                title="Simulate Live Alert",
                                class_name="hover:text-indigo-600 transition-colors",
                            ),
                            class_name="flex items-center",
                        ),
                        class_name="flex items-center justify-between mb-2 px-3 pt-3",
                    ),
                    rx.scroll_area(
                        rx.el.div(
                            rx.cond(
                                NotificationPaginationState.paginated_notifications.length()
                                > 0,
                                rx.foreach(
                                    NotificationPaginationState.paginated_notifications,
                                    alert_card,
                                ),
                                rx.el.div(
                                    rx.icon(
                                        "bell-off",
                                        size=24,
                                        class_name="text-gray-300 mb-2",
                                    ),
                                    rx.el.p(
                                        "No active alerts",
                                        class_name="text-[10px] font-bold text-gray-400 uppercase",
                                    ),
                                    class_name="flex flex-col items-center justify-center h-full opacity-60",
                                ),
                            ),
                            class_name="flex flex-col gap-2 p-2 min-h-0",
                        ),
                        type="hover",
                        scrollbars="vertical",
                        class_name="flex-1 w-full",
                        style={"height": "calc(100vh - 200px)"},
                    ),
                    pagination_footer(),
                    class_name="h-full w-full flex flex-col min-w-[220px]",
                ),
                class_name="h-full w-full overflow-hidden",
            ),
            class_name=rx.cond(
                PortfolioDashboardState.is_sidebar_open,
                "fixed inset-y-0 right-0 w-80 max-w-full shadow-2xl md:shadow-none md:static md:w-[220px] opacity-100 border-l border-gray-200",
                "w-0 opacity-0 border-l-0 pointer-events-none fixed inset-y-0 right-0 md:static",
            )
            + " flex bg-[#F9F9F9] h-full shrink-0 flex-col z-40 overflow-hidden transition-all duration-300 ease-in-out",
        )
    )