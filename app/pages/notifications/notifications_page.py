import reflex as rx
from app.components.shared.sidebar import sidebar
from app.components.shared.mobile_nav import mobile_nav
from app.states.notifications.notification_state import NotificationState, Notification


def notification_card(notification: Notification) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    notification["icon"], size=24, class_name=notification["color"]
                ),
                class_name=f"w-12 h-12 rounded-full {notification['color'].replace('text', 'bg')}/10 flex items-center justify-center shrink-0",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h4(
                        notification["title"], class_name="font-bold text-gray-900"
                    ),
                    rx.el.span(
                        notification["time_ago"],
                        class_name="text-xs text-gray-400 font-medium",
                    ),
                    class_name="flex items-center justify-between mb-1",
                ),
                rx.el.p(
                    notification["message"],
                    class_name="text-sm text-gray-600 leading-relaxed",
                ),
                class_name="flex flex-col flex-1",
            ),
            class_name="flex gap-4 items-start",
        ),
        rx.el.div(
            rx.cond(
                ~notification["is_read"],
                rx.el.button(
                    rx.icon("check", size=16),
                    on_click=lambda: NotificationState.mark_read(notification["id"]),
                    class_name="p-2 text-indigo-600 hover:bg-indigo-50 rounded-lg transition-colors",
                    title="Mark as read",
                ),
            ),
            class_name="ml-4 flex flex-col justify-center",
        ),
        class_name=rx.cond(
            notification["is_read"],
            "p-6 bg-white rounded-2xl border border-gray-100 flex justify-between group opacity-75",
            "p-6 bg-white rounded-2xl border-l-4 border-l-indigo-500 border-y border-r border-gray-100 shadow-sm flex justify-between group",
        ),
    )


def category_button(category: str) -> rx.Component:
    return rx.el.button(
        category,
        on_click=lambda: NotificationState.set_category(category),
        class_name=rx.cond(
            NotificationState.selected_category == category,
            "px-4 py-2 rounded-xl text-sm font-bold bg-indigo-600 text-white shadow-lg shadow-indigo-200 transition-all",
            "px-4 py-2 rounded-xl text-sm font-bold text-gray-500 hover:bg-white hover:text-gray-900 transition-all",
        ),
    )


def notifications_page() -> rx.Component:
    return rx.el.div(
        sidebar(current_page="Notifications"),
        rx.el.main(
            mobile_nav(current_page="Notifications"),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "Notifications",
                            class_name="text-2xl font-bold text-gray-900 mb-1",
                        ),
                        rx.el.p(
                            "Stay updated with your portfolio activity and alerts.",
                            class_name="text-gray-500 text-sm",
                        ),
                        class_name="flex flex-col",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.icon("check-check", size=18, class_name="mr-2"),
                            "Mark all read",
                            on_click=NotificationState.mark_all_read,
                            class_name="flex items-center px-4 py-2 text-sm font-bold text-gray-600 hover:bg-white rounded-xl transition-colors border border-transparent hover:border-gray-200",
                        ),
                        rx.el.button(
                            rx.icon("trash-2", size=18, class_name="mr-2"),
                            "Clear all",
                            on_click=NotificationState.clear_all,
                            class_name="flex items-center px-4 py-2 text-sm font-bold text-red-600 hover:bg-red-50 rounded-xl transition-colors",
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    class_name="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-8",
                ),
                rx.el.div(
                    rx.foreach(NotificationState.categories, category_button),
                    class_name="flex flex-wrap gap-2 mb-8 p-1.5 bg-gray-100/50 rounded-2xl w-fit",
                ),
                rx.cond(
                    NotificationState.filtered_notifications.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            NotificationState.filtered_notifications, notification_card
                        ),
                        class_name="flex flex-col gap-4 max-w-3xl",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon(
                                "bell-off", size=48, class_name="text-gray-300 mb-4"
                            ),
                            rx.el.h3(
                                "No notifications",
                                class_name="text-lg font-bold text-gray-900",
                            ),
                            rx.el.p(
                                "You're all caught up! Check back later for updates.",
                                class_name="text-gray-500 text-sm mt-1",
                            ),
                            class_name="flex flex-col items-center justify-center py-20 bg-white rounded-3xl border border-dashed border-gray-200",
                        )
                    ),
                ),
                class_name="max-w-7xl mx-auto",
            ),
            class_name="flex-1 bg-gray-50/50 h-screen overflow-y-auto p-4 md:p-8",
        ),
        class_name="flex w-full h-screen font-['Inter'] bg-white text-gray-900",
    )