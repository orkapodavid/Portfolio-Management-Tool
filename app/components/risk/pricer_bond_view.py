import reflex as rx
from app.states.risk.pricer_bond_state import PricerBondState
from .risk_views import header_cell, text_cell

def pricer_bond_view() -> rx.Component:
    return rx.el.div(
        # Top Section: Terms and Pricing Results (Original layout preserved in a wrapper)
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Terms", class_name="text-sm font-bold mb-4 bg-gray-100 p-2 rounded"
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label("Valuation Date", class_name="font-bold block mb-1"),
                        rx.el.input(
                            type="date", class_name="border rounded p-1 w-full text-xs"
                        ),
                    ),
                    rx.el.div(
                        rx.el.label("Coupon Rate", class_name="font-bold block mb-1"),
                        rx.el.input(class_name="border rounded p-1 w-full text-xs"),
                    ),
                    class_name="grid grid-cols-1 gap-4 text-xs",
                ),
                class_name="w-1/3 p-4 border-r border-gray-200 overflow-y-auto",
            ),
            rx.el.div(
                rx.el.h3(
                    "Pricing Results",
                    class_name="text-sm font-bold mb-4 bg-gray-100 p-2 rounded",
                ),
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            header_cell("Ticker"),
                            header_cell("Spot Price"),
                            header_cell("Fair Value"),
                            header_cell("Discount"),
                        )
                    ),
                    rx.el.tbody(
                        rx.el.tr(
                            text_cell("AAPL 4.5% 2029"),
                            text_cell("98.50"),
                            text_cell("99.25"),
                            text_cell("0.75%"),
                        )
                    ),
                    class_name="w-full table-auto border-separate border-spacing-0",
                ),
                class_name="flex-1 p-4",
            ),
            class_name="flex w-full h-1/2 bg-white",
        ),

        # Middle Section: Visualization Controls
        rx.el.div(
            rx.el.div(
                rx.text("X-Axis:", class_name="text-sm font-bold mr-2"),
                rx.select(
                    ["Maturity", "Coupon", "Duration"],
                    value=PricerBondState.x_axis,
                    on_change=PricerBondState.set_x_axis,
                    class_name="border rounded p-1 text-xs"
                ),
                class_name="flex items-center"
            ),
            rx.el.div(
                rx.text("Y-Axis:", class_name="text-sm font-bold mr-2"),
                rx.select(
                    ["Yield", "Price", "Convexity"],
                    value=PricerBondState.y_axis,
                    on_change=PricerBondState.set_y_axis,
                    class_name="border rounded p-1 text-xs"
                ),
                class_name="flex items-center"
            ),
            rx.el.div(
                rx.text("Z-Axis:", class_name="text-sm font-bold mr-2"),
                rx.select(
                    ["None", "Price", "Spread"],
                    value=PricerBondState.z_axis,
                    on_change=PricerBondState.set_z_axis,
                    class_name="border rounded p-1 text-xs"
                ),
                class_name="flex items-center"
            ),
            class_name="flex gap-6 p-4 bg-gray-50 border-t border-b border-gray-200"
        ),

        # Bottom Section: Chart
        rx.el.div(
            rx.plotly(data=PricerBondState.chart, style={"width": "100%", "height": "100%"}),
            class_name="w-full h-1/2 p-4"
        ),

        class_name="flex flex-col w-full h-full bg-white"
    )
