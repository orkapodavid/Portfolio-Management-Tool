import reflex as rx
from app.states.risk.pricer_warrant_state import PricerWarrantState
from .risk_views import header_cell, text_cell

def pricer_warrant_view() -> rx.Component:
    return rx.el.div(
        # Top Section: Terms and Simulations (Original layout preserved in a wrapper)
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
                        rx.el.label("Effective Date", class_name="font-bold block mb-1"),
                        rx.el.input(
                            type="date", class_name="border rounded p-1 w-full text-xs"
                        ),
                    ),
                    rx.el.div(
                        rx.el.label("Maturity Date", class_name="font-bold block mb-1"),
                        rx.el.input(
                            type="date", class_name="border rounded p-1 w-full text-xs"
                        ),
                    ),
                    rx.el.div(
                        rx.el.label("Underlying", class_name="font-bold block mb-1"),
                        rx.el.input(class_name="border rounded p-1 w-full text-xs"),
                    ),
                    rx.el.div(
                        rx.el.label("Maturity Ticker", class_name="font-bold block mb-1"),
                        rx.el.input(class_name="border rounded p-1 w-full text-xs"),
                    ),
                    rx.el.div(
                        rx.el.label("Spot Price", class_name="font-bold block mb-1"),
                        rx.el.input(class_name="border rounded p-1 w-full text-xs"),
                    ),
                    rx.el.div(
                        rx.el.label("Strike Price", class_name="font-bold block mb-1"),
                        rx.el.input(class_name="border rounded p-1 w-full text-xs"),
                    ),
                    rx.el.div(
                        rx.el.label("Hit Fee Dec", class_name="font-bold block mb-1"),
                        rx.el.input(class_name="border rounded p-1 w-full text-xs"),
                    ),
                    rx.el.div(
                        rx.el.label("Currency", class_name="font-bold block mb-1"),
                        rx.el.input(class_name="border rounded p-1 w-full text-xs"),
                    ),
                    rx.el.div(
                        rx.el.label("Hit Rate", class_name="font-bold block mb-1"),
                        rx.el.input(class_name="border rounded p-1 w-full text-xs"),
                    ),
                    rx.el.div(
                        rx.el.label("Interest Rate", class_name="font-bold block mb-1"),
                        rx.el.input(class_name="border rounded p-1 w-full text-xs"),
                    ),
                    class_name="grid grid-cols-2 gap-4 text-xs",
                ),
                class_name="w-1/3 p-4 border-r border-gray-200 overflow-y-auto",
            ),
            rx.el.div(
                rx.el.h3(
                    "Simulations & Outputs",
                    class_name="text-sm font-bold mb-4 bg-gray-100 p-2 rounded",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(header_cell("Simulation#"), header_cell("Jump to 0"))
                        ),
                        rx.el.tbody(rx.el.tr(text_cell("1"), text_cell("No"))),
                        class_name="w-full table-auto border-separate border-spacing-0 mb-4",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.span("Fair Value:", class_name="font-bold mr-2"),
                            rx.el.span("$45.20", class_name="font-mono text-green-600"),
                            class_name="text-lg mb-2",
                        ),
                        rx.el.div(
                            rx.el.span("Delta:", class_name="font-bold mr-2"),
                            rx.el.span("0.65", class_name="font-mono text-gray-700"),
                            class_name="text-md",
                        ),
                        class_name="p-4 bg-gray-50 rounded border border-gray-200",
                    ),
                    class_name="flex flex-col gap-4",
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
                    ["Spot Price", "Strike", "Volatility"],
                    value=PricerWarrantState.x_axis,
                    on_change=PricerWarrantState.set_x_axis,
                    class_name="border rounded p-1 text-xs"
                ),
                class_name="flex items-center"
            ),
            rx.el.div(
                rx.text("Y-Axis:", class_name="text-sm font-bold mr-2"),
                rx.select(
                    ["Value", "Delta", "Gamma"],
                    value=PricerWarrantState.y_axis,
                    on_change=PricerWarrantState.set_y_axis,
                    class_name="border rounded p-1 text-xs"
                ),
                class_name="flex items-center"
            ),
            rx.el.div(
                rx.text("Z-Axis:", class_name="text-sm font-bold mr-2"),
                rx.select(
                    ["None", "Time", "Volatility"],
                    value=PricerWarrantState.z_axis,
                    on_change=PricerWarrantState.set_z_axis,
                    class_name="border rounded p-1 text-xs"
                ),
                class_name="flex items-center"
            ),
            class_name="flex gap-6 p-4 bg-gray-50 border-t border-b border-gray-200"
        ),

        # Bottom Section: Chart
        rx.el.div(
            rx.plotly(data=PricerWarrantState.chart, style={"width": "100%", "height": "100%"}),
            class_name="w-full h-1/2 p-4"
        ),

        class_name="flex flex-col w-full h-full bg-white"
    )
