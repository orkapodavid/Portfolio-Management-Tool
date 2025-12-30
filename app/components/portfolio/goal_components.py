import reflex as rx
from app.states.portfolio.goals_state import GoalsState, Goal


def goal_progress_bar(current: float, target: float, color: str) -> rx.Component:
    raw_pct = current / target * 100
    pct = rx.cond(
        target > 0, rx.cond(raw_pct > 100, 100, rx.cond(raw_pct < 0, 0, raw_pct)), 0
    )
    bg_color = rx.match(
        color,
        ("indigo", "bg-indigo-500"),
        ("emerald", "bg-emerald-500"),
        ("blue", "bg-blue-500"),
        ("amber", "bg-amber-500"),
        ("gray", "bg-gray-500"),
        "bg-indigo-500",
    )
    return rx.el.div(
        rx.el.div(
            class_name=f"h-full rounded-full {bg_color} transition-all duration-500",
            style={"width": f"{pct}%"},
        ),
        class_name="w-full h-2.5 bg-gray-100 rounded-full overflow-hidden",
    )


def goal_card(goal: Goal) -> rx.Component:
    pct = goal["current_amount"] / goal["target_amount"] * 100
    pct_str = f"{pct:.1f}%"
    icon_bg = rx.match(
        goal["color"],
        ("indigo", "bg-indigo-100 text-indigo-600"),
        ("emerald", "bg-emerald-100 text-emerald-600"),
        ("blue", "bg-blue-100 text-blue-600"),
        ("amber", "bg-amber-100 text-amber-600"),
        "bg-gray-100 text-gray-600",
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(goal["icon"], size=24),
                    class_name=f"p-3 rounded-xl {icon_bg}",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("pencil", size=16),
                        on_click=lambda: GoalsState.open_edit_modal(goal),
                        class_name="p-2 text-gray-400 hover:text-indigo-600 hover:bg-gray-50 rounded-lg transition-colors",
                    ),
                    rx.el.button(
                        rx.icon("trash-2", size=16),
                        on_click=lambda: GoalsState.delete_goal(goal["id"]),
                        class_name="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg transition-colors",
                    ),
                    class_name="flex gap-1",
                ),
                class_name="flex justify-between items-start mb-4",
            ),
            rx.el.h3(goal["name"], class_name="text-lg font-bold text-gray-900 mb-1"),
            rx.el.p(
                goal["category"],
                class_name="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "Progress", class_name="text-sm font-medium text-gray-500"
                    ),
                    rx.el.span(pct_str, class_name="text-sm font-bold text-gray-900"),
                    class_name="flex justify-between mb-2",
                ),
                goal_progress_bar(
                    goal["current_amount"], goal["target_amount"], goal["color"]
                ),
                class_name="mb-6",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p("Current", class_name="text-xs text-gray-500 mb-1"),
                    rx.el.p(
                        f"${goal['current_amount']:,.0f}",
                        class_name="text-sm font-bold text-gray-900",
                    ),
                ),
                rx.el.div(
                    rx.el.p(
                        "Target", class_name="text-xs text-gray-500 mb-1 text-right"
                    ),
                    rx.el.p(
                        f"${goal['target_amount']:,.0f}",
                        class_name="text-sm font-bold text-gray-900 text-right",
                    ),
                ),
                class_name="flex justify-between items-end border-t border-gray-100 pt-4",
            ),
            class_name="flex flex-col",
        ),
        class_name="bg-white p-6 rounded-3xl border border-gray-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] hover:shadow-[0_20px_40px_rgb(0,0,0,0.08)] transition-all duration-300 group",
    )


def add_edit_goal_modal() -> rx.Component:
    return rx.cond(
        GoalsState.is_modal_open,
        rx.el.div(
            rx.el.div(
                class_name="fixed inset-0 bg-gray-900/60 backdrop-blur-sm transition-opacity z-[100]",
                on_click=GoalsState.close_modal,
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        rx.cond(GoalsState.editing_goal_id, "Edit Goal", "New Goal"),
                        class_name="text-xl font-bold text-gray-900",
                    ),
                    rx.el.button(
                        rx.icon("x", size=20, class_name="text-gray-400"),
                        on_click=GoalsState.close_modal,
                        class_name="p-2 hover:bg-gray-100 rounded-full transition-colors",
                    ),
                    class_name="flex items-center justify-between mb-8",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.label(
                            "Goal Name",
                            class_name="block text-sm font-bold text-gray-700 mb-2",
                        ),
                        rx.el.input(
                            name="name",
                            default_value=GoalsState.form_name,
                            placeholder="e.g., Retirement, Dream Car",
                            class_name="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all font-medium",
                            required=True,
                        ),
                        class_name="mb-5",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Category",
                            class_name="block text-sm font-bold text-gray-700 mb-2",
                        ),
                        rx.el.select(
                            rx.foreach(
                                GoalsState.categories,
                                lambda c: rx.el.option(c, value=c),
                            ),
                            name="category",
                            default_value=GoalsState.form_category,
                            class_name="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all font-medium bg-white appearance-none",
                        ),
                        class_name="mb-5",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Target Amount",
                                class_name="block text-sm font-bold text-gray-700 mb-2",
                            ),
                            rx.el.input(
                                name="target_amount",
                                type="number",
                                default_value=GoalsState.form_target.to_string(),
                                class_name="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all font-medium",
                                required=True,
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Current Amount",
                                class_name="block text-sm font-bold text-gray-700 mb-2",
                            ),
                            rx.el.input(
                                name="current_amount",
                                type="number",
                                default_value=GoalsState.form_current.to_string(),
                                class_name="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all font-medium",
                                required=True,
                            ),
                        ),
                        class_name="grid grid-cols-2 gap-5 mb-5",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Monthly Contribution",
                                class_name="block text-sm font-bold text-gray-700 mb-2",
                            ),
                            rx.el.input(
                                name="monthly_contribution",
                                type="number",
                                default_value=GoalsState.form_contribution.to_string(),
                                class_name="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all font-medium",
                                required=True,
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Deadline",
                                class_name="block text-sm font-bold text-gray-700 mb-2",
                            ),
                            rx.el.input(
                                name="deadline",
                                type="date",
                                default_value=GoalsState.form_deadline,
                                class_name="w-full px-4 py-3 rounded-xl border border-gray-200 focus:border-indigo-500 focus:ring-4 focus:ring-indigo-500/10 outline-none transition-all font-medium",
                                required=True,
                            ),
                        ),
                        class_name="grid grid-cols-2 gap-5 mb-8",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancel",
                            type="button",
                            on_click=GoalsState.close_modal,
                            class_name="px-6 py-2.5 text-sm font-bold text-gray-600 hover:bg-gray-50 rounded-xl transition-colors",
                        ),
                        rx.el.button(
                            "Save Goal",
                            type="submit",
                            class_name="px-6 py-2.5 text-sm font-bold text-white bg-gradient-to-r from-indigo-600 to-violet-600 hover:shadow-lg hover:shadow-indigo-500/30 rounded-xl transition-all duration-200 transform hover:-translate-y-0.5",
                        ),
                        class_name="flex items-center justify-end gap-3",
                    ),
                    on_submit=GoalsState.save_goal,
                ),
                class_name="bg-white rounded-3xl shadow-2xl w-full max-w-lg p-8 relative z-[101] animate-in fade-in zoom-in duration-300 scale-100",
            ),
            class_name="fixed inset-0 z-[100] flex items-center justify-center p-4",
        ),
    )