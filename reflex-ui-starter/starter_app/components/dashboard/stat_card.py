"""
Stat Card — Reusable stat card component for Dashboard.

Renders a metric card with label, value, and change indicator.
"""

import reflex as rx
from starter_app.constants import POSITIVE_GREEN, NEGATIVE_RED


def stat_card(label: str, value: str, change: str = "", is_positive: bool = True) -> rx.Component:
    """Reusable stat card component.

    Args:
        label: Metric label (e.g. "Total Users")
        value: Metric value (e.g. "1,234")
        change: Optional change text (e.g. "+12%")
        is_positive: Whether the change is positive (green) or negative (red)
    """
    return rx.el.div(
        rx.el.p(
            label,
            class_name="text-[10px] font-medium text-gray-500 uppercase tracking-wide",
        ),
        rx.el.div(
            rx.el.span(
                value,
                class_name="text-xl font-bold text-gray-900",
            ),
            rx.cond(
                change != "",
                rx.el.span(
                    change,
                    class_name=f"ml-2 text-xs font-medium {'text-green-600' if is_positive else 'text-red-600'}",
                ),
                rx.fragment(),
            ),
            class_name="flex items-baseline gap-1 mt-1",
        ),
        class_name="bg-white rounded-lg border border-gray-100 p-4 shadow-sm hover:shadow-md transition-shadow",
    )


def stat_card_dynamic(
    label: rx.Var[str],
    value: rx.Var[str],
    change: rx.Var[str] = "",
    is_positive: rx.Var[bool] = True,
) -> rx.Component:
    """Dynamic stat card that binds to state vars.

    Use this when label/value come from state variables.
    """
    return rx.el.div(
        rx.el.p(
            label,
            class_name="text-[10px] font-medium text-gray-500 uppercase tracking-wide",
        ),
        rx.el.div(
            rx.el.span(
                value,
                class_name="text-xl font-bold text-gray-900",
            ),
            class_name="flex items-baseline gap-1 mt-1",
        ),
        class_name="bg-white rounded-lg border border-gray-100 p-4 shadow-sm hover:shadow-md transition-shadow",
    )
