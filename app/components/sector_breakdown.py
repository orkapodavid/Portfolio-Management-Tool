import reflex as rx
from app.states.portfolio_state import PortfolioState
from app.components.allocation_chart import legend_item


def sector_breakdown() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Sector Breakdown", class_name="text-lg font-bold text-gray-900"),
            class_name="mb-6",
        ),
        rx.el.div(
            rx.recharts.pie_chart(
                rx.recharts.pie(
                    data=PortfolioState.sector_breakdown,
                    data_key="value",
                    name_key="name",
                    cx="50%",
                    cy="50%",
                    inner_radius=60,
                    outer_radius=85,
                    padding_angle=2,
                    stroke="#fff",
                    stroke_width=2,
                ),
                rx.recharts.tooltip(),
                height=300,
                width="100%",
            ),
            class_name="flex items-center justify-center w-full relative",
        ),
        rx.el.div(
            rx.foreach(PortfolioState.sector_breakdown, legend_item),
            class_name="flex flex-wrap gap-4 justify-center mt-4",
        ),
        class_name="bg-white rounded-2xl p-6 border border-gray-100 shadow-sm h-fit",
    )