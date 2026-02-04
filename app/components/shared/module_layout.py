import reflex as rx
from app.components.shared.top_navigation import top_navigation
from app.components.shared.performance_header import performance_header
from app.components.shared.notification_sidebar import notification_sidebar
from app.constants import FINANCIAL_GREY, DEFAULT_FONT


def sub_tab_link(name: str, base_url: str, current_subtab: str) -> rx.Component:
    """A subtab link using rx.link."""
    slug = name.lower().replace(" ", "-").replace("/", "-")
    # Handle special cases if any, e.g. mapping "Trade Summary (War/Bond)" to "trade-summary"
    # For now assuming simple slugification matches the route

    # Remove parens for cleaner URL
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


def workspace_controls(state_class, current_module: str) -> rx.Component:
    """
    Workspace controls (Search, Refresh, etc.) bound to the specific State class.
    Assumes state_class has standard methods:
    - set_search/set_current_search
    - refresh_data/refresh_prices
    - etc.
    """
    # Note: We are using getattr/checking if methods exist on the class instance in Python is tricky at compile time.
    # We assume standard naming conventions for the refactored states.
    # For PnLState: set_pnl_change_search etc. Wait, mixins have specific search logic.
    # The Main State should ideally expose a unified `set_search` that delegates, OR we bind to the attribute directly.
    # But we don't know WHICH subtab is active easily here for binding specific attribute names string-wise.

    # COMPROMISE: For this refactor, we will rely on the State Class having a unified `set_module_search` or similar,
    # OR we use the `PortfolioDashboardState` for shared controls TEMPORARILY if the new states don't have a unified interface yet.
    # The `PortfolioDashboardState` is still part of the app.

    # However, to be "route-based", each page might need its own controls if they differ.
    # Let's try to bind to `state_class.set_search` if we standardize on that?
    # In my mixins I named them `set_pnl_change_search` etc.
    # I should add a `set_search` method to `ModuleState` that delegates.

    # Let's revert to wrapping `PortfolioDashboardState` logic for controls for now,
    # as `PortfolioDashboardState` is still imported and used by legacy components.
    # BUT `module_layout` is for NEW pages.
    # Let's simple bind to `state_class.set_search` (I will add this to the State classes).

    return rx.el.div(
        # ... Simplified controls ...
        # For simplicity in this step, I'll render a placeholder controls bar or minimal implementation
        # to avoid breaking compilation with missing methods.
        rx.el.div(
            rx.el.div(
                rx.el.button(
                    rx.icon("refresh-cw", size=12),
                    # on_click=state_class.refresh_data, # naming to be standardized
                    class_name="h-6 w-6 flex items-center justify-center bg-white border border-gray-200 text-gray-600 rounded hover:bg-gray-50 hover:text-blue-600 shadow-sm",
                ),
                # Search
                rx.el.div(
                    rx.icon(
                        "search", size=12, class_name="text-gray-400 mr-1.5 shrink-0"
                    ),
                    rx.el.input(
                        placeholder="Search...",
                        # on_change=state_class.set_search, # naming to be standardized
                        class_name="bg-transparent text-[10px] font-bold outline-none w-full text-gray-700 placeholder-gray-400",
                    ),
                    class_name="flex items-center bg-white border border-gray-200 rounded px-2 h-6 flex-1 max-w-[200px] shadow-sm ml-2",
                ),
                class_name="flex items-center gap-2 flex-1",
            ),
            class_name="flex items-center justify-between px-3 py-1.5 bg-[#F9F9F9] border-b border-gray-200 shrink-0 h-[40px]",
        )
    )


def module_layout(
    content: rx.Component,
    module_name: str,
    subtab_name: str,
    subtabs: list[str],
    # state_class: type[rx.State] = None, # Optional for now
) -> rx.Component:
    """
    Layout wrapper for all module pages.
    """
    module_slug = module_name.lower().replace(" ", "-")

    return rx.el.div(
        top_navigation(),  # This still uses PortfolioDashboardState for now, needs Phase 3 update
        performance_header(),
        rx.el.div(
            # Contextual Workspace replacement
            rx.el.div(
                rx.el.div(
                    rx.foreach(
                        subtabs,
                        lambda name: sub_tab_link(name, module_slug, subtab_name),
                    ),
                    class_name="flex flex-row items-center bg-white border-b border-gray-200 px-2 pt-0.5 overflow-hidden shrink-0 h-[28px] w-full max-w-full flex-nowrap",
                ),
                # NOTE: workspace_controls removed - AG Grid components now include
                # their own grid_toolbar from ag_grid_config.py
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
