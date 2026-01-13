import reflex as rx
from app.states.portfolio.portfolio_state import PortfolioState


def legend_item(item: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="w-3 h-3 rounded-full mr-2 shadow-sm ring-2 ring-white",
            background_color=item["fill"],
        ),
        rx.el.span(item["name"], class_name="text-xs text-gray-600 font-semibold"),
        class_name="flex items-center bg-gray-50 px-3 py-1.5 rounded-full border border-gray-100",
    )
