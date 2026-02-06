import reflex as rx
from app.states.notifications import NotificationSidebarState, NotificationItem


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
                on_click=NotificationSidebarState.dismiss_notification(notification["id"]),
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
                on_click=NotificationSidebarState.mark_notification_read(notification["id"]),
                title="Mark as read",
                class_name="p-1 rounded hover:bg-white/60 text-gray-700 transition-colors",
            ),
            rx.el.button(
                rx.icon("arrow-right", size=12),
                on_click=NotificationSidebarState.navigate_to_item(notification["id"]),
                title="Go to details",
                class_name="p-1 rounded hover:bg-white/60 text-gray-700 transition-colors",
            ),
            class_name="flex gap-1 mt-2 pt-2 border-t border-black/10",
        ),
        class_name=f"{bg_color} {card_opacity} p-3 rounded-md border-l-4 {border_color} shadow-sm hover:shadow-md transition-all duration-300 animate-in slide-in-from-right fade-in",
    )


def scroll_sentinel() -> rx.Component:
    """Invisible sentinel element that triggers loading more notifications.
    
    Uses IntersectionObserver to detect when user scrolls near the bottom.
    """
    # JavaScript to set up IntersectionObserver for infinite scroll
    observer_script = """
    (() => {
        const sentinel = document.getElementById('scroll-sentinel');
        if (!sentinel) return;
        
        // Avoid duplicate observers
        if (sentinel.dataset.observed === 'true') return;
        sentinel.dataset.observed = 'true';
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    // Trigger the Reflex event
                    const event = new CustomEvent('load-more');
                    sentinel.dispatchEvent(event);
                }
            });
        }, {
            root: sentinel.closest('[data-scroll-area]'),
            rootMargin: '100px',
            threshold: 0.1
        });
        
        observer.observe(sentinel);
    })()
    """
    
    return rx.el.div(
        rx.cond(
            NotificationSidebarState.is_loading_more,
            rx.el.div(
                rx.icon("loader-circle", size=16, class_name="animate-spin text-gray-400"),
                rx.el.span("Loading...", class_name="text-[9px] text-gray-400"),
                class_name="flex items-center justify-center gap-2 py-2",
            ),
            rx.cond(
                NotificationSidebarState.has_more_notifications,
                rx.el.div(
                    rx.el.span(
                        f"Scroll for more • {NotificationSidebarState.visible_notifications.length()} of {NotificationSidebarState.total_notifications_count}",
                        class_name="text-[8px] text-gray-400",
                    ),
                    class_name="text-center py-2",
                ),
            ),
        ),
        id="scroll-sentinel",
        on_click=NotificationSidebarState.load_more_notifications,  # Fallback click
        class_name="min-h-[20px]",
    )


def filter_tab(label: str, filter_val: str) -> rx.Component:
    is_active = NotificationSidebarState.notification_filter == filter_val
    return rx.el.button(
        label,
        on_click=lambda: NotificationSidebarState.set_notification_filter(filter_val),
        class_name=rx.cond(
            is_active,
            "px-2 py-1 bg-blue-600 text-white rounded text-[8px] font-black uppercase shadow-sm",
            "px-2 py-1 bg-gray-200 text-gray-600 rounded text-[8px] font-bold uppercase hover:bg-gray-300 transition-colors",
        ),
    )


def notification_sidebar() -> rx.Component:
    """The right sidebar component for notifications (Region 4) with infinite scroll."""
    # Import UIState only for sidebar visibility toggle
    from app.states.ui.ui_state import UIState

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
                                    NotificationSidebarState.unread_count.to_string(),
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
                                    on_click=NotificationSidebarState.add_simulated_notification,
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
                                NotificationSidebarState.visible_notifications.length() > 0,
                                rx.fragment(
                                    rx.foreach(
                                        NotificationSidebarState.visible_notifications,
                                        alert_card,
                                    ),
                                    scroll_sentinel(),
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
                        style={"height": "calc(100vh - 160px)"},
                        # Trigger load more when scrolling near bottom
                        on_scroll=NotificationSidebarState.load_more_notifications,
                    ),
                    # Footer with count instead of pagination
                    rx.el.div(
                        rx.el.span(
                            f"Showing {NotificationSidebarState.visible_notifications.length()} of {NotificationSidebarState.total_notifications_count}",
                            class_name="text-[9px] font-bold text-gray-500",
                        ),
                        class_name="flex items-center justify-center px-3 py-2 border-t border-gray-200 bg-white/80 backdrop-blur-sm",
                    ),
                    class_name="h-full w-full flex flex-col min-w-[220px]",
                ),
                class_name="h-full w-full overflow-hidden",
            ),
            class_name=rx.cond(
                UIState.is_sidebar_open,
                "fixed inset-y-0 right-0 w-80 max-w-full shadow-2xl md:shadow-none md:static md:w-[220px] opacity-100 border-l border-gray-200",
                "w-0 opacity-0 border-l-0 pointer-events-none fixed inset-y-0 right-0 md:static",
            )
            + " flex bg-[#F9F9F9] h-full shrink-0 flex-col z-40 overflow-hidden transition-all duration-300 ease-in-out",
        ),
        on_mount=NotificationSidebarState.load_notifications,
    )
