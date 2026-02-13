import reflex as rx
from starter_app.components.shared.top_navigation import top_navigation
from starter_app.components.shared.app_header import app_header
from starter_app.components.shared.notification_sidebar import notification_sidebar
from starter_app.constants import FINANCIAL_GREY, DEFAULT_FONT


def sub_tab_link(name: str, base_url: str, current_subtab: str) -> rx.Component:
    """A subtab link using rx.link."""
    slug = name.lower().replace(" ", "-").replace("/", "-")
    slug = slug.replace("(", "").replace(")", "")
    url = f"/{base_url}/{slug}"
    is_active = current_subtab == name

    return rx.link(
        rx.el.button(
            name,
            class_name=rx.cond(
                is_active,
                "px-3 h-full text-[9px] font-black text-blue-600 border-b-2 border-blue-600 uppercase tracking-tighter whitespace-nowrap",
                "px-3 h-full text-[9px] font-bold text-gray-400 border-b-2 border-transparent hover:text-gray-600 uppercase tracking-tighter whitespace-nowrap",
            ),
        ),
        href=url,
        class_name="h-full flex items-center",
    )


def module_layout(
    content: rx.Component,
    module_name: str,
    subtab_name: str,
    subtabs: list[str],
) -> rx.Component:
    """
    Layout wrapper for all module pages.
    """
    module_slug = module_name.lower().replace(" ", "-")

    return rx.el.div(
        top_navigation(),
        app_header(),
        rx.el.div(
            # Contextual Workspace
            rx.el.div(
                rx.el.div(
                    rx.foreach(
                        subtabs,
                        lambda name: sub_tab_link(name, module_slug, subtab_name),
                    ),
                    class_name="flex flex-row items-center bg-white border-b border-gray-200 px-2 pt-0.5 overflow-hidden shrink-0 h-[28px] w-full max-w-full flex-nowrap",
                ),
                rx.el.div(
                    content,
                    class_name="flex-1 flex flex-col min-h-0 overflow-hidden bg-white",
                ),
                class_name="flex flex-col flex-1 min-h-0 h-full border-r border-gray-200",
            ),
            notification_sidebar(),
            class_name=f"flex flex-1 overflow-hidden min-h-0 bg-[{FINANCIAL_GREY}] w-full",
        ),
        class_name=f"flex flex-col h-screen w-screen bg-[{FINANCIAL_GREY}] font-['{DEFAULT_FONT}'] antialiased overflow-hidden",
    )
