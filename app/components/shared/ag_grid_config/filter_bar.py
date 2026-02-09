"""
Reusable filter bar components for AG Grids.

Provides date range filter bars with Apply/Clear buttons,
and shared CSS class constants for consistent styling.
"""

import reflex as rx


# =============================================================================
# SHARED CSS CLASSES
# =============================================================================

FILTER_LABEL_CLASS = "text-[10px] font-semibold text-gray-500 uppercase tracking-wider"
FILTER_INPUT_CLASS = (
    "h-7 px-2 text-[11px] bg-white border border-gray-200 rounded "
    "text-gray-700 focus:outline-none focus:ring-1 focus:ring-blue-400 "
    "focus:border-blue-400 transition-colors"
)
FILTER_BTN_CLASS = (
    "h-7 px-3 text-[10px] font-bold uppercase tracking-wider rounded "
    "transition-all flex items-center gap-1 shadow-sm cursor-pointer"
)


# =============================================================================
# COMPONENTS
# =============================================================================


def filter_date_input(
    label: str,
    value: rx.Var[str],
    on_change,
) -> rx.Component:
    """A labelled date input for filter bars."""
    return rx.el.div(
        rx.el.span(label, class_name=FILTER_LABEL_CLASS),
        rx.el.input(
            type="date",
            value=value,
            on_change=on_change,
            class_name=f"{FILTER_INPUT_CLASS} w-[130px]",
        ),
        class_name="flex items-center gap-1.5",
    )


def filter_date_range_bar(
    *,
    from_value: rx.Var[str],
    to_value: rx.Var[str],
    on_from_change,
    on_to_change,
    on_apply,
    has_active_filters: rx.Var[bool],
    on_clear,
    extra_left_content: rx.Component | None = None,
) -> rx.Component:
    """
    Reusable date-range filter bar with Apply / Clear buttons.

    Args:
        from_value: State var for the FROM date.
        to_value: State var for the TO date.
        on_from_change: Handler when FROM date changes.
        on_to_change: Handler when TO date changes.
        on_apply: Handler when Apply is clicked.
        has_active_filters: Var controlling Clear button visibility.
        on_clear: Handler when Clear is clicked.
        extra_left_content: Optional component inserted before the date
            inputs (e.g. a ticker popover).  A vertical divider is
            automatically added after it.
    """
    left_items: list[rx.Component] = []

    if extra_left_content is not None:
        left_items.append(extra_left_content)
        # vertical divider
        left_items.append(rx.el.div(class_name="w-px h-5 bg-gray-200 mx-1"))

    left_items.append(filter_date_input("From", from_value, on_from_change))
    left_items.append(filter_date_input("To", to_value, on_to_change))

    return rx.el.div(
        rx.el.div(
            # LEFT — optional extra + date range
            rx.el.div(
                *left_items,
                class_name="flex items-center gap-2",
            ),
            # RIGHT — Apply + Clear buttons
            rx.el.div(
                rx.el.button(
                    rx.icon("search", size=12),
                    rx.el.span("Apply"),
                    on_click=on_apply,
                    class_name=(
                        f"{FILTER_BTN_CLASS} bg-gradient-to-r from-blue-600 to-indigo-600 "
                        "text-white hover:shadow-md"
                    ),
                ),
                rx.cond(
                    has_active_filters,
                    rx.el.button(
                        rx.icon("x", size=12),
                        rx.el.span("Clear"),
                        on_click=on_clear,
                        class_name=(
                            f"{FILTER_BTN_CLASS} bg-white border border-gray-200 "
                            "text-gray-500 hover:text-red-500 hover:border-red-300"
                        ),
                    ),
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        class_name=(
            "px-3 py-2 bg-gradient-to-r from-gray-50/80 to-slate-50/80 "
            "border border-gray-100 rounded-lg backdrop-blur-sm"
        ),
    )
