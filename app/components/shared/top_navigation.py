import reflex as rx
from app.states.dashboard.portfolio_dashboard_state import PortfolioDashboardState
from app.constants import NAV_HEIGHT, NAV_BG, ICON_NAV_SIZE


def nav_button(module_name: str, icon_name: str) -> rx.Component:
    is_active = PortfolioDashboardState.active_module == module_name
    return rx.el.button(
        rx.el.div(
            rx.icon(
                icon_name,
                size=ICON_NAV_SIZE,
                class_name=rx.cond(is_active, "text-white", "text-gray-400"),
            ),
            rx.el.span(
                module_name,
                class_name=rx.cond(
                    is_active,
                    "text-[9px] font-bold text-white uppercase",
                    "text-[9px] font-medium text-gray-400 hover:text-gray-200 uppercase",
                ),
            ),
            rx.cond(
                is_active,
                rx.el.div(
                    class_name="absolute bottom-0 left-0 right-0 h-0.5 bg-blue-500 animate-pulse"
                ),
            ),
            class_name="flex flex-row items-center gap-1.5 relative",
        ),
        on_click=PortfolioDashboardState.set_module(module_name),
        class_name=rx.cond(
            is_active,
            "px-2 h-full border-b-2 border-blue-500 bg-white/10 relative",
            "px-2 h-full border-b-2 border-transparent hover:bg-white/5",
        ),
    )


def mobile_menu_item(module_name: str, icon_name: str) -> rx.Component:
    is_active = PortfolioDashboardState.active_module == module_name
    return rx.el.button(
        rx.icon(
            icon_name,
            size=18,
            class_name=rx.cond(is_active, "text-blue-500", "text-gray-500"),
        ),
        rx.el.span(
            module_name,
            class_name=rx.cond(
                is_active,
                "text-sm font-bold text-blue-600",
                "text-sm font-medium text-gray-600",
            ),
        ),
        on_click=PortfolioDashboardState.set_module(module_name),
        class_name=rx.cond(
            is_active,
            "flex items-center gap-3 w-full p-3 rounded-lg bg-blue-50 border border-blue-100",
            "flex items-center gap-3 w-full p-3 rounded-lg hover:bg-gray-50 border border-transparent",
        ),
    )


def top_navigation() -> rx.Component:
    """Compacted top navigation bar (Region 1). Height 40px."""
    return rx.el.nav(
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    rx.icon(
                        "menu", size=18, class_name="text-gray-300 hover:text-white"
                    ),
                    on_click=PortfolioDashboardState.toggle_mobile_menu,
                    class_name="md:hidden mr-3 p-1 shrink-0",
                ),
                rx.icon("activity", size=16, class_name="text-blue-400"),
                rx.el.h1(
                    "PMT",
                    class_name="text-[10px] font-black text-white tracking-widest",
                ),
                class_name="flex items-center gap-2 mr-2 px-2 border-r border-gray-700 h-full shrink-0",
            ),
            rx.el.div(
                rx.foreach(
                    PortfolioDashboardState.module_icons.entries(),
                    lambda item: nav_button(item[0], item[1]),
                ),
                class_name="hidden md:flex items-center h-full overflow-x-auto no-scrollbar gap-0 ml-2",
            ),
            rx.el.div(
                rx.el.button(
                    rx.el.div(
                        rx.icon(
                            "bell",
                            size=16,
                            class_name="text-gray-400 group-hover:text-white",
                        ),
                        rx.cond(
                            PortfolioDashboardState.unread_count > 0,
                            rx.el.span(
                                PortfolioDashboardState.unread_count.to_string(),
                                class_name=f"absolute -top-1 -right-1 flex h-2.5 w-2.5 items-center justify-center rounded-full bg-red-500 text-[7px] font-black text-white ring-1 ring-[{NAV_BG}] animate-pulse",
                            ),
                        ),
                        class_name="relative",
                    ),
                    on_click=PortfolioDashboardState.toggle_sidebar,
                    class_name=rx.cond(
                        PortfolioDashboardState.is_sidebar_open,
                        "group p-1 rounded-md bg-white/20 text-white transition-all duration-200",
                        "group p-1 rounded-md hover:bg-white/10 transition-all duration-200",
                    ),
                ),
                rx.icon(
                    "user",
                    size=16,
                    class_name="text-gray-400 hover:text-white cursor-pointer ml-1",
                ),
                class_name="ml-auto flex items-center gap-1 px-2 border-l border-gray-700 h-full shrink-0",
            ),
            class_name="flex items-center h-full w-full max-w-full",
        ),
        rx.cond(
            PortfolioDashboardState.is_mobile_menu_open,
            rx.el.div(
                rx.el.div(
                    class_name="fixed inset-0 bg-black/50 z-[60]",
                    on_click=PortfolioDashboardState.toggle_mobile_menu,
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "MODULES",
                            class_name="text-xs font-black text-gray-400 uppercase tracking-widest mb-4",
                        ),
                        rx.el.div(
                            rx.foreach(
                                PortfolioDashboardState.module_icons.entries(),
                                lambda item: mobile_menu_item(item[0], item[1]),
                            ),
                            class_name="flex flex-col gap-2",
                        ),
                        class_name="p-4 overflow-y-auto h-full",
                    ),
                    class_name="fixed inset-y-0 left-0 w-64 bg-white shadow-2xl z-[70] animate-in slide-in-from-left duration-200 border-r border-gray-200",
                ),
            ),
        ),
        class_name=f"w-full h-[{NAV_HEIGHT}] bg-[{NAV_BG}] shadow-md z-[60] shrink-0",
    )