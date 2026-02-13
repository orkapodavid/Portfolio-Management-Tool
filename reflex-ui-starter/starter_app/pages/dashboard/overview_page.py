"""
Dashboard Overview Page — Uses DashboardState and extracted components.

Demonstrates the mixin state architecture:
- DashboardState.load_overview_data() loads from UserService (via core_pkg)
- stat_card and activity_feed extracted as reusable components
"""

import reflex as rx
from starter_app.states.ui.ui_state import UIState
from starter_app.states.dashboard import DashboardState
from starter_app.components.shared.module_layout import module_layout
from starter_app.components.dashboard.stat_card import stat_card
from starter_app.components.dashboard.activity_feed import activity_feed
from starter_app.constants import POSITIVE_GREEN, NEGATIVE_RED


def overview_content() -> rx.Component:
    """Main content for the overview tab."""
    return rx.el.div(
        # Welcome banner
        rx.el.div(
            rx.el.div(
                rx.icon("sparkles", size=20, class_name="text-blue-500"),
                rx.el.div(
                    rx.el.h2("Welcome to Starter App", class_name="text-sm font-black text-gray-800"),
                    rx.el.p(
                        "This is a demo dashboard page. Data is loaded from core_pkg services via mixin states.",
                        class_name="text-[11px] text-gray-500 mt-0.5",
                    ),
                    class_name="flex flex-col",
                ),
                class_name="flex items-start gap-3",
            ),
            class_name="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-100 rounded-lg p-4 mb-4",
        ),
        # Stat cards — using extracted components and DashboardState
        rx.el.div(
            stat_card("Total Users", DashboardState.total_users.to(str), "+12.5%", True),
            stat_card("Active Users", DashboardState.active_users.to(str), DashboardState.active_user_pct, True),
            stat_card("Active Sessions", "1,423", "-2.1%", False),
            stat_card("Conversion", "3.24%", "+0.5%", True),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 mb-4",
        ),
        # Content area with chart placeholder + activity feed from state
        rx.el.div(
            rx.el.div(
                rx.el.h3("Activity Chart", class_name="text-[10px] font-black text-gray-400 uppercase tracking-widest mb-2"),
                rx.el.div(
                    rx.icon("bar-chart-3", size=48, class_name="text-gray-200"),
                    rx.el.p("Chart component placeholder", class_name="text-xs text-gray-400 mt-2"),
                    class_name="flex flex-col items-center justify-center h-[200px]",
                ),
                class_name="bg-white rounded-lg p-4 border border-gray-200 shadow-sm flex-1",
            ),
            # Activity feed using extracted component and DashboardState
            rx.el.div(
                activity_feed(DashboardState.recent_activity),
                class_name="w-full md:w-[300px]",
            ),
            class_name="flex flex-col md:flex-row gap-3",
        ),
        on_mount=DashboardState.load_overview_data,
        class_name="p-4 overflow-y-auto flex-1",
    )


def overview_page() -> rx.Component:
    """Dashboard Overview page wrapped in module_layout."""
    return module_layout(
        content=overview_content(),
        module_name="Dashboard",
        subtab_name="Overview",
        subtabs=UIState.MODULE_SUBTABS["Dashboard"],
    )
