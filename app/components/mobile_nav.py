import reflex as rx
from app.states.mobile_nav_state import MobileNavState


def mobile_nav_item(
    text: str, icon: str, href: str = "#", active: bool = False
) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(
                icon,
                class_name=rx.cond(
                    active,
                    "text-indigo-600",
                    "text-gray-400 group-hover:text-indigo-500",
                ),
                size=20,
            ),
            rx.el.span(text, class_name="font-medium tracking-tight"),
            rx.cond(
                active,
                rx.el.div(
                    class_name="absolute left-0 top-1/2 -translate-y-1/2 w-1 h-8 bg-indigo-600 rounded-r-full"
                ),
            ),
            class_name=rx.cond(
                active,
                "flex items-center gap-3 px-4 py-3 rounded-xl bg-indigo-50/80 text-indigo-700 transition-all duration-200 relative overflow-hidden",
                "flex items-center gap-3 px-4 py-3 rounded-xl text-gray-500 hover:bg-gray-50 hover:text-gray-900 transition-all duration-200 group",
            ),
        ),
        href=href,
        on_click=MobileNavState.close_menu,
        class_name="block mb-1.5",
    )


def mobile_nav(current_page: str) -> rx.Component:
    return rx.fragment(
        rx.el.div(
            rx.el.button(
                rx.icon("menu", size=24, class_name="text-gray-700"),
                on_click=MobileNavState.toggle_menu,
                class_name="p-2 hover:bg-gray-100 rounded-lg transition-colors",
            ),
            rx.el.div(
                rx.icon("chart-line", class_name="text-indigo-600 mr-2", size=20),
                rx.el.span(
                    "InvestFlow",
                    class_name="text-lg font-bold text-gray-900 tracking-tight",
                ),
                class_name="flex items-center",
            ),
            rx.el.div(
                rx.image(
                    src="https://api.dicebear.com/9.x/notionists/svg?seed=Felix",
                    class_name="h-8 w-8 rounded-full bg-indigo-50 ring-2 ring-white shadow-sm",
                ),
                class_name="flex items-center",
            ),
            class_name="md:hidden flex items-center justify-between px-4 py-3 bg-white/80 backdrop-blur-md border-b border-gray-100 sticky top-0 z-30 -mx-4 -mt-4 mb-6",
        ),
        rx.cond(
            MobileNavState.is_open,
            rx.el.div(
                rx.el.div(
                    class_name="fixed inset-0 bg-gray-900/60 backdrop-blur-sm z-40 animate-in fade-in duration-200",
                    on_click=MobileNavState.close_menu,
                ),
                rx.el.aside(
                    rx.el.div(
                        rx.el.div(
                            rx.el.div(
                                rx.el.div(
                                    rx.icon(
                                        "chart-line", class_name="text-white", size=20
                                    ),
                                    class_name="h-8 w-8 bg-gradient-to-br from-indigo-500 to-violet-600 rounded-lg flex items-center justify-center shadow-lg shadow-indigo-200",
                                ),
                                rx.el.span(
                                    "InvestFlow",
                                    class_name="text-xl font-bold text-gray-900 tracking-tight",
                                ),
                                class_name="flex items-center gap-3",
                            ),
                            rx.el.button(
                                rx.icon("x", size=20, class_name="text-gray-400"),
                                on_click=MobileNavState.close_menu,
                                class_name="p-2 hover:bg-gray-100 rounded-lg transition-colors",
                            ),
                            class_name="flex items-center justify-between mb-8 px-2",
                        ),
                        rx.el.nav(
                            rx.el.div(
                                rx.el.p(
                                    "MENU",
                                    class_name="px-4 text-[10px] font-bold text-gray-400 mb-4 tracking-widest uppercase",
                                ),
                                mobile_nav_item(
                                    "Dashboard",
                                    "layout-dashboard",
                                    href="/",
                                    active=current_page == "Dashboard",
                                ),
                                mobile_nav_item(
                                    "Portfolios",
                                    "pie-chart",
                                    href="/portfolios",
                                    active=current_page == "Portfolios",
                                ),
                                mobile_nav_item(
                                    "Watchlist",
                                    "eye",
                                    href="/watchlist",
                                    active=current_page == "Watchlist",
                                ),
                                mobile_nav_item(
                                    "Research",
                                    "search",
                                    href="/research",
                                    active=current_page == "Research",
                                ),
                                mobile_nav_item(
                                    "Reports",
                                    "file-text",
                                    href="/reports",
                                    active=current_page == "Reports",
                                ),
                                mobile_nav_item(
                                    "Goals",
                                    "target",
                                    href="/goals",
                                    active=current_page == "Goals",
                                ),
                                class_name="mb-8",
                            ),
                            rx.el.div(
                                rx.el.p(
                                    "SETTINGS",
                                    class_name="px-4 text-[10px] font-bold text-gray-400 mb-4 tracking-widest uppercase",
                                ),
                                mobile_nav_item(
                                    "Profile",
                                    "user",
                                    href="/profile",
                                    active=current_page == "Profile",
                                ),
                                mobile_nav_item(
                                    "Notifications",
                                    "bell",
                                    href="/notifications",
                                    active=current_page == "Notifications",
                                ),
                                mobile_nav_item(
                                    "Settings",
                                    "settings",
                                    href="/settings",
                                    active=current_page == "Settings",
                                ),
                            ),
                            class_name="flex-1 overflow-y-auto scrollbar-hide",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.image(
                                    src="https://api.dicebear.com/9.x/notionists/svg?seed=Felix",
                                    class_name="h-10 w-10 rounded-full bg-indigo-50 ring-2 ring-white shadow-sm",
                                ),
                                rx.el.div(
                                    rx.el.p(
                                        "Alex Morgan",
                                        class_name="text-sm font-bold text-gray-900",
                                    ),
                                    rx.el.p(
                                        "Pro Investor",
                                        class_name="text-xs text-indigo-500 font-medium",
                                    ),
                                    class_name="flex flex-col",
                                ),
                                class_name="flex items-center gap-3",
                            ),
                            class_name="mt-auto mx-2 p-3 bg-gray-50 border border-gray-100 rounded-2xl flex items-center justify-between shadow-sm",
                        ),
                        class_name="flex flex-col h-full p-6",
                    ),
                    class_name="fixed inset-y-0 left-0 w-80 bg-white z-50 shadow-2xl animate-in slide-in-from-left duration-300",
                ),
                class_name="md:hidden relative z-50",
            ),
        ),
    )