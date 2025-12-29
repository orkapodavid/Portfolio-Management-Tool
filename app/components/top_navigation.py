import reflex as rx
from app.states.portfolio_dashboard_state import PortfolioDashboardState


def nav_button(module_name: str, icon_name: str) -> rx.Component:
    """Creates a navigation button for a module."""
    is_active = PortfolioDashboardState.active_module == module_name
    return rx.el.button(
        rx.el.div(
            rx.icon(
                icon_name,
                size=16,
                class_name=rx.cond(is_active, "text-white", "text-gray-400"),
            ),
            rx.el.span(
                module_name,
                class_name=rx.cond(
                    is_active,
                    "text-xs font-bold text-white tracking-wide",
                    "text-xs font-medium text-gray-400 hover:text-gray-200",
                ),
            ),
            class_name="flex flex-col items-center gap-1",
        ),
        on_click=lambda: PortfolioDashboardState.set_module(module_name),
        class_name=rx.cond(
            is_active,
            "px-4 py-2 h-full border-b-2 border-blue-500 bg-white/10 transition-colors duration-200",
            "px-4 py-2 h-full border-b-2 border-transparent hover:bg-white/5 transition-colors duration-200",
        ),
    )


def top_navigation() -> rx.Component:
    """The top navigation bar component (Region 1)."""
    return rx.el.nav(
        rx.el.div(
            rx.el.div(
                rx.icon("activity", size=20, class_name="text-blue-400"),
                rx.el.h1(
                    "REFLEX", class_name="text-lg font-bold text-white tracking-wider"
                ),
                rx.el.span(
                    "PORTFOLIO",
                    class_name="text-xs font-light text-gray-400 self-end mb-1",
                ),
                class_name="flex items-center gap-2 mr-8 px-4 border-r border-gray-700 h-full",
            ),
            rx.el.div(
                rx.foreach(
                    PortfolioDashboardState.module_icons,
                    lambda item: nav_button(item[0], item[1]),
                ),
                class_name="flex items-center h-full overflow-x-auto no-scrollbar",
            ),
            rx.el.div(
                rx.el.button(
                    rx.el.div(
                        rx.icon(
                            "bell",
                            size=18,
                            class_name="text-gray-400 group-hover:text-white",
                        ),
                        rx.cond(
                            PortfolioDashboardState.unread_count > 0,
                            rx.el.span(
                                PortfolioDashboardState.unread_count,
                                class_name="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-red-500 text-[10px] font-bold text-white shadow-sm",
                            ),
                        ),
                        class_name="relative",
                    ),
                    on_click=PortfolioDashboardState.toggle_sidebar,
                    class_name="group relative p-2 rounded-full hover:bg-white/10 transition-colors",
                ),
                rx.icon(
                    "user",
                    size=18,
                    class_name="text-gray-400 hover:text-white cursor-pointer",
                ),
                class_name="ml-auto flex items-center gap-4 px-6 border-l border-gray-700 h-full",
            ),
            class_name="flex items-center h-full w-full max-w-[1920px] mx-auto",
        ),
        class_name="w-full h-16 bg-[#333333] shadow-md z-50 shrink-0",
    )