"""
Activity Feed — Recent activity list component for Dashboard.

Renders a vertical feed of recent activity events.
"""

import reflex as rx


def _activity_icon(color: str) -> rx.Component:
    """Small colored dot indicator."""
    return rx.el.div(
        class_name=f"w-2 h-2 rounded-full bg-{color}-500 mt-1.5 shrink-0",
    )


def _activity_row(item: dict) -> rx.Component:
    """Single activity feed row."""
    return rx.el.div(
        _activity_icon(item["color"]),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    item["user"],
                    class_name="text-xs font-semibold text-gray-800",
                ),
                rx.el.span(
                    item["time"],
                    class_name="text-[10px] text-gray-400 ml-auto",
                ),
                class_name="flex items-center justify-between",
            ),
            rx.el.p(
                item["detail"],
                class_name="text-[11px] text-gray-500 mt-0.5",
            ),
            class_name="flex-1 min-w-0",
        ),
        class_name="flex gap-2 py-2 border-b border-gray-50 last:border-b-0",
    )


def activity_feed(items: rx.Var) -> rx.Component:
    """Activity feed component.

    Args:
        items: State var containing list of ActivityItem dicts.
    """
    return rx.el.div(
        rx.el.h3(
            "Recent Activity",
            class_name="text-sm font-bold text-gray-800 mb-3",
        ),
        rx.foreach(items, _activity_row),
        class_name="bg-white rounded-lg border border-gray-100 p-4 shadow-sm",
    )
