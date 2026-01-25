"""
Shared table components for market data views.

Contains reusable header_cell and text_cell components.
"""

import reflex as rx
from app.states.market_data.market_data_state import MarketDataState


def header_cell(text: str, align: str = "left", column_key: str = "") -> rx.Component:
    """
    Creates a sortable header cell for tables.

    Args:
        text: Header text to display
        align: Text alignment (left, center, right)
        column_key: Column key for sorting, empty string disables sorting
    """
    align_class = rx.match(
        align, ("right", "text-right"), ("center", "text-center"), "text-left"
    )
    sort_icon = rx.cond(
        MarketDataState.sort_column == column_key,
        rx.cond(
            MarketDataState.sort_direction == "asc",
            rx.icon("arrow-up", size=10, class_name="ml-1 text-blue-600"),
            rx.icon("arrow-down", size=10, class_name="ml-1 text-blue-600"),
        ),
        rx.icon(
            "arrow-up-down",
            size=10,
            class_name="ml-1 text-gray-300 opacity-0 group-hover:opacity-100 transition-opacity",
        ),
    )
    return rx.el.th(
        rx.el.div(
            text,
            rx.cond(column_key != "", sort_icon, rx.fragment()),
            class_name=f"flex items-center {rx.match(align, ('right', 'justify-end'), ('center', 'justify-center'), 'justify-start')}",
        ),
        on_click=lambda: rx.cond(
            column_key, MarketDataState.toggle_sort(column_key), None
        ),
        class_name=f"px-3 py-3 {align_class} text-[10px] font-bold text-gray-700 uppercase tracking-widest border-b-2 border-gray-400 bg-[#E5E7EB] sticky top-0 z-30 shadow-sm h-[44px] whitespace-nowrap cursor-pointer hover:bg-gray-200 transition-colors group select-none",
    )


def text_cell(
    val: str, align: str = "left", bold: bool = False, clickable: bool = False
) -> rx.Component:
    """
    Creates a standard text cell for tables.

    Args:
        val: Cell value to display
        align: Text alignment (left, center, right)
        bold: Whether to use bold font
        clickable: Whether to style as a clickable link
    """
    base_class = f"px-3 py-2 text-[10px] text-gray-700 text-{align} border-b border-gray-200 align-middle whitespace-nowrap"
    if clickable:
        return rx.el.td(
            rx.el.a(val, class_name="text-blue-600 hover:underline cursor-pointer"),
            class_name=base_class,
        )
    weight = rx.cond(bold, "font-black", "font-medium")
    return rx.el.td(val, class_name=f"{base_class} {weight}")
