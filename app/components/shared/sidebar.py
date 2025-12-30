import reflex as rx


def sidebar_item(
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
        class_name="block mb-1.5",
    )


def sidebar(current_page: str = "Dashboard") -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("chart-line", class_name="text-white", size=22),
                    class_name="h-10 w-10 bg-gradient-to-br from-indigo-500 to-violet-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-200 ring-2 ring-indigo-50 ring-offset-2",
                ),
                rx.el.span(
                    "InvestFlow",
                    class_name="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600 tracking-tight",
                ),
                class_name="flex items-center gap-3 px-2 mb-12",
            ),
            rx.el.nav(
                rx.el.div(
                    rx.el.p(
                        "MENU",
                        class_name="px-4 text-[10px] font-bold text-gray-400 mb-4 tracking-widest uppercase",
                    ),
                    sidebar_item(
                        "Dashboard",
                        "layout-dashboard",
                        href="/",
                        active=current_page == "Dashboard",
                    ),
                    sidebar_item(
                        "Portfolios",
                        "pie-chart",
                        href="/portfolios",
                        active=current_page == "Portfolios",
                    ),
                    sidebar_item(
                        "Watchlist",
                        "eye",
                        href="/watchlist",
                        active=current_page == "Watchlist",
                    ),
                    sidebar_item(
                        "Research",
                        "search",
                        href="/research",
                        active=current_page == "Research",
                    ),
                    sidebar_item(
                        "Reports",
                        "file-text",
                        href="/reports",
                        active=current_page == "Reports",
                    ),
                    sidebar_item(
                        "Goals", "target", href="/goals", active=current_page == "Goals"
                    ),
                    class_name="mb-10",
                ),
                rx.el.div(
                    rx.el.p(
                        "SETTINGS",
                        class_name="px-4 text-[10px] font-bold text-gray-400 mb-4 tracking-widest uppercase",
                    ),
                    sidebar_item(
                        "Profile",
                        "user",
                        href="/profile",
                        active=current_page == "Profile",
                    ),
                    sidebar_item(
                        "Notifications",
                        "bell",
                        href="/notifications",
                        active=current_page == "Notifications",
                    ),
                    sidebar_item(
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
                            "Alex Morgan", class_name="text-sm font-bold text-gray-900"
                        ),
                        rx.el.p(
                            "Pro Investor",
                            class_name="text-xs text-indigo-500 font-medium",
                        ),
                        class_name="flex flex-col",
                    ),
                    class_name="flex items-center gap-3",
                ),
                rx.el.button(
                    rx.icon(
                        "log-out",
                        class_name="text-gray-400 group-hover:text-red-500 transition-colors",
                        size=20,
                    ),
                    class_name="p-2 hover:bg-red-50 rounded-lg transition-colors group",
                ),
                class_name="mt-auto mx-2 p-3 bg-gradient-to-br from-gray-50 to-white border border-gray-100 rounded-2xl flex items-center justify-between shadow-sm",
            ),
            class_name="flex flex-col h-full p-6 relative",
        ),
        class_name="w-72 h-screen bg-white/80 backdrop-blur-xl border-r border-gray-100 hidden md:block shrink-0 sticky top-0 z-20",
    )