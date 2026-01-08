import reflex as rx
from app.states.dashboard.portfolio_dashboard_state import (
    PortfolioDashboardState,
    NotificationItem,
)


def alert_card(notification: NotificationItem) -> rx.Component:
    """Enhanced notification card with actions and read status."""
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
    card_opacity = rx.cond(notification["read"], "opacity-60", "opacity-100")
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.cond(
                    ~notification["read"],
                    rx.el.div(class_name="w-1.5 h-1.5 bg-blue-600 rounded-full mr-1.5"),
                ),
                rx.el.h4(
                    notification["header"],
                    class_name=f"text-[11px] font-black {text_color} leading-tight uppercase tracking-wider",
                ),
                class_name="flex items-center",
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
        rx.el.div(
            rx.el.button(
                rx.icon("check", size=12),
                on_click=PortfolioDashboardState.mark_notification_read(
                    notification["id"]
                ),
                title="Mark as read",
                class_name="p-1 rounded hover:bg-white/60 text-gray-700 transition-colors",
            ),
            rx.el.button(
                rx.icon("arrow-right", size=12),
                on_click=lambda: PortfolioDashboardState.navigate_to_notification(
                    notification["id"]
                ),
                title="Go to details",
                class_name="p-1 rounded hover:bg-white/60 text-gray-700 transition-colors",
            ),
            class_name="flex gap-1 mt-2 pt-2 border-t border-black/10",
        ),
        class_name=f"{bg_color} {card_opacity} p-3 rounded-md border-l-4 {border_color} shadow-sm hover:shadow-md transition-all duration-300 animate-in slide-in-from-right fade-in",
    )


def pagination_footer() -> rx.Component:
    return rx.el.div(
        rx.el.button(
            rx.el.div(
                rx.icon("chevron-left", size=12),
                rx.el.span("Prev", class_name="ml-1"),
                class_name="flex items-center",
            ),
            on_click=PortfolioDashboardState.prev_notification_page,
            disabled=PortfolioDashboardState.notification_page == 1,
            class_name="px-2 py-1 rounded hover:bg-gray-200 disabled:opacity-30 disabled:cursor-not-allowed transition-all text-[9px] font-black uppercase tracking-tighter",
        ),
        rx.el.span(
            f"{PortfolioDashboardState.notification_page} / {PortfolioDashboardState.total_notification_pages}",
            class_name="text-[10px] font-black text-gray-600 tabular-nums",
        ),
        rx.el.button(
            rx.el.div(
                rx.el.span("Next", class_name="mr-1"),
                rx.icon("chevron-right", size=12),
                class_name="flex items-center",
            ),
            on_click=PortfolioDashboardState.next_notification_page,
            disabled=PortfolioDashboardState.notification_page
            == PortfolioDashboardState.total_notification_pages,
            class_name="px-2 py-1 rounded hover:bg-gray-200 disabled:opacity-30 disabled:cursor-not-allowed transition-all text-[9px] font-black uppercase tracking-tighter",
        ),
        class_name="flex items-center justify-between px-3 py-2 border-t border-gray-200 bg-white/80 backdrop-blur-sm sticky bottom-0",
    )


def filter_tab(label: str, filter_val: str) -> rx.Component:
    is_active = PortfolioDashboardState.notification_filter == filter_val
    return rx.el.button(
        label,
        on_click=lambda: PortfolioDashboardState.set_notification_filter(filter_val),
        class_name=rx.cond(
            is_active,
            "px-2 py-1 bg-blue-600 text-white rounded text-[8px] font-black uppercase shadow-sm",
            "px-2 py-1 bg-gray-200 text-gray-600 rounded text-[8px] font-bold uppercase hover:bg-gray-300 transition-colors",
        ),
    )


def notification_sidebar() -> rx.Component:
    """The right sidebar component for notifications (Region 4) with filtering."""
    return rx.el.aside(
        rx.el.div(
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
                                    PortfolioDashboardState.unread_count.to_string(),
                                    class_name="ml-2 bg-blue-600 text-white text-[8px] font-black px-1.5 py-0.5 rounded-full",
                                ),
                                class_name="flex items-center",
                            ),
                            rx.el.div(
                                rx.el.button(
                                    rx.icon(
                                        "circle_plus",
                                        size=12,
                                        class_name="text-gray-400",
                                    ),
                                    on_click=PortfolioDashboardState.add_simulated_notification,
                                    title="Simulate Live Alert",
                                    class_name="hover:text-indigo-600 transition-colors",
                                ),
                                class_name="flex items-center",
                            ),
                            class_name="flex items-center justify-between mb-2 px-3 pt-3",
                        ),
                        rx.el.div(
                            filter_tab("All", "all"),
                            filter_tab("Alerts", "alert"),
                            filter_tab("Info", "info"),
                            class_name="flex gap-1 px-3 pb-2 border-b border-gray-200",
                        ),
                    ),
                    rx.scroll_area(
                        rx.el.div(
                            rx.cond(
                                PortfolioDashboardState.paginated_notifications.length()
                                > 0,
                                rx.foreach(
                                    PortfolioDashboardState.paginated_notifications,
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