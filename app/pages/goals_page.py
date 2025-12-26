import reflex as rx
from app.components.sidebar import sidebar
from app.components.mobile_nav import mobile_nav
from app.states.goals_state import GoalsState
from app.components.goal_components import goal_card, add_edit_goal_modal


def stat_card(
    label: str, value: str, subtext: str, color_scheme: str = "indigo"
) -> rx.Component:
    bg_class = f"bg-{color_scheme}-50"
    text_class = f"text-{color_scheme}-600"
    return rx.el.div(
        rx.el.p(
            label,
            class_name="text-xs font-bold text-gray-500 uppercase tracking-wide mb-1",
        ),
        rx.el.h3(value, class_name="text-2xl font-bold text-gray-900 mb-1"),
        rx.el.p(subtext, class_name=f"text-xs font-bold {text_class}"),
        class_name=f"p-5 rounded-2xl border border-{color_scheme}-100 {bg_class}",
    )


def goals_page() -> rx.Component:
    return rx.el.div(
        sidebar(current_page="Goals"),
        add_edit_goal_modal(),
        rx.el.main(
            mobile_nav(current_page="Goals"),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h1(
                            "Financial Goals",
                            class_name="text-2xl font-bold text-gray-900",
                        ),
                        rx.el.p(
                            "Track and manage your long-term financial objectives.",
                            class_name="text-gray-500 text-sm mt-1",
                        ),
                        class_name="flex flex-col",
                    ),
                    rx.el.button(
                        rx.icon("plus", size=16, class_name="mr-2"),
                        "Add New Goal",
                        on_click=GoalsState.open_add_modal,
                        class_name="flex items-center bg-indigo-600 text-white px-5 py-2.5 rounded-xl text-sm font-bold hover:bg-indigo-700 transition-colors shadow-lg shadow-indigo-200 hover:-translate-y-0.5 transform duration-200",
                    ),
                    class_name="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8",
                ),
                rx.el.div(
                    stat_card(
                        "Total Saved",
                        f"${GoalsState.total_goals_value:,.0f}",
                        "Across all goals",
                        "indigo",
                    ),
                    stat_card(
                        "Goals On Track",
                        f"{GoalsState.goals_on_track}",
                        f"Out of {GoalsState.goals.length()} active goals",
                        "emerald",
                    ),
                    stat_card(
                        "Monthly Contribution",
                        "$6,800",
                        "Projected for this month",
                        "blue",
                    ),
                    class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10",
                ),
                rx.cond(
                    GoalsState.goals.length() > 0,
                    rx.el.div(
                        rx.foreach(GoalsState.goals, goal_card),
                        class_name="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.icon("target", size=48, class_name="text-gray-300 mb-4"),
                            rx.el.h3(
                                "No goals set yet",
                                class_name="text-lg font-bold text-gray-900",
                            ),
                            rx.el.p(
                                "Start planning your future by adding your first goal.",
                                class_name="text-gray-500 text-sm mt-1 mb-6",
                            ),
                            rx.el.button(
                                "Create Goal",
                                on_click=GoalsState.open_add_modal,
                                class_name="px-6 py-2.5 bg-indigo-600 text-white font-bold rounded-xl hover:bg-indigo-700 transition-colors",
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