import reflex as rx
from app.states.portfolio_dashboard_state import PortfolioDashboardState
from app.constants import NAV_HEIGHT, NAV_BG, ICON_NAV_SIZE


def nav_button(module_name: str, icon_name: str) -> rx.Component:
    """Creates an ultra-compact navigation button with inline icon and text."""
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
                    "text-[9px] font-bold text-white tracking-tighter uppercase whitespace-nowrap",
                    "text-[9px] font-medium text-gray-400 hover:text-gray-200 uppercase whitespace-nowrap",
                ),
            ),
            class_name="flex flex-row items-center gap-1.5",
        ),
        on_click=PortfolioDashboardState.set_module(module_name),
        title=module_name,
        class_name=rx.cond(
            is_active,
            "px-2 h-full border-b-2 border-blue-500 bg-white/10 transition-colors duration-75 flex items-center",
            "px-2 h-full border-b-2 border-transparent hover:bg-white/5 transition-colors duration-75 flex items-center",
        ),
    )


def top_navigation() -> rx.Component:
    """Compacted top navigation bar (Region 1). Height 40px."""
    return rx.el.nav(
        rx.el.div(
            rx.el.div(
                rx.icon("activity", size=16, class_name="text-blue-400"),
                rx.el.h1(
                    "REFLEX",
                    class_name="text-[10px] font-black text-white tracking-widest",
                ),
                class_name="flex items-center gap-2 mr-2 px-2 border-r border-gray-700 h-full shrink-0",
            ),
            rx.el.div(
                rx.foreach(
                    PortfolioDashboardState.module_icons.entries(),
                    lambda item: nav_button(item[0], item[1]),
                ),
                class_name="flex items-center h-full overflow-x-auto no-scrollbar gap-0",
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
        class_name=f"w-full h-[{NAV_HEIGHT}] bg-[{NAV_BG}] shadow-md z-[60] shrink-0",
    )