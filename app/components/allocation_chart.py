import reflex as rx
from app.states.dashboard_state import DashboardState


def legend_item(item: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="w-3 h-3 rounded-full mr-2", background_color=item["fill"]
        ),
        rx.el.span(item["name"], class_name="text-xs text-gray-600 font-medium"),
        class_name="flex items-center",
    )


def legend_item(item: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            class_name="w-3 h-3 rounded-full mr-2 shadow-sm ring-2 ring-white",
            background_color=item["fill"],
        ),
        rx.el.span(item["name"], class_name="text-xs text-gray-600 font-semibold"),
        class_name="flex items-center bg-gray-50 px-3 py-1.5 rounded-full border border-gray-100",
    )


def allocation_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3("Asset Allocation", class_name="text-xl font-bold text-gray-900"),
            rx.el.button(
                rx.icon("gallery_thumbnails", size=20, class_name="text-gray-400"),
                class_name="p-2 hover:bg-gray-50 rounded-xl transition-colors",
            ),
            class_name="flex items-center justify-between mb-8",
        ),
        rx.el.div(
            rx.recharts.pie_chart(
                rx.recharts.pie(
                    data=DashboardState.asset_allocation_data,
                    data_key="value",
                    name_key="name",
                    cx="50%",
                    cy="50%",
                    inner_radius=70,
                    outer_radius=95,
                    padding_angle=3,
                    stroke="#fff",
                    stroke_width=3,
                ),
                rx.recharts.tooltip(
                    content_style={
                        "backgroundColor": "rgba(255, 255, 255, 0.95)",
                        "borderRadius": "16px",
                        "border": "none",
                        "boxShadow": "0 10px 25px -5px rgba(0, 0, 0, 0.1)",
                        "padding": "12px",
                    },
                    item_style={"fontWeight": "600", "color": "#374151"},
                ),
                height=300,
                width="100%",
            ),
            class_name="flex items-center justify-center w-full relative drop-shadow-sm",
        ),
        rx.el.div(
            rx.foreach(DashboardState.asset_allocation_data, legend_item),
            class_name="flex flex-wrap gap-2 justify-center mt-6",
        ),
        class_name="bg-white rounded-3xl p-8 border border-gray-100 shadow-[0_8px_30px_rgb(0,0,0,0.04)] h-full flex flex-col",
    )