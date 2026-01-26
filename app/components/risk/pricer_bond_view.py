import reflex as rx
from app.states.risk.pricer_bond_state import PricerBondState
from .risk_views import header_cell, text_cell

def pricer_bond_view() -> rx.Component:
    return rx.el.div(
        # Top Section: Terms and Pricing Results
        rx.el.div(
            # Left Column: Terms
            rx.el.div(
                rx.el.h3(
                    "Terms", class_name="text-sm font-bold mb-4 bg-gray-100 p-2 rounded"
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label("Valuation Date", class_name="font-bold block mb-1"),
                        rx.el.input(
                            type="date",
                            class_name="border rounded p-1 w-full text-xs",
                            value=PricerBondState.valuation_date,
                            on_change=PricerBondState.set_valuation_date
                        ),
                    ),
                    rx.el.div(
                        rx.el.label("Coupon Rate", class_name="font-bold block mb-1"),
                        rx.el.input(
                            type="number",
                            placeholder="e.g. 5.0",
                            class_name="border rounded p-1 w-full text-xs",
                            value=PricerBondState.coupon_rate,
                            on_change=PricerBondState.set_coupon_rate
                        ),
                    ),
                    class_name="grid grid-cols-1 gap-4 text-xs",
                ),
                class_name="w-1/3 p-4 border-r border-gray-200 overflow-y-auto",
            ),
            # Right Column: Pricing Results
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
            class_name="flex w-full h-1/2 bg-white border-b border-gray-200",
        ),

        # Bottom Section: Chart and Controls
        rx.card(
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.text("X-Axis", font_size="0.8rem", weight="bold"),
                        rx.select(
                            ["Maturity", "Duration"],
                            value=PricerBondState.x_axis,
                            on_change=PricerBondState.set_x_axis,
                        ),
                    ),
                    rx.vstack(
                        rx.text("Y-Axis", font_size="0.8rem", weight="bold"),
                        rx.select(
                            ["Yield", "Price"],
                            value=PricerBondState.y_axis,
                            on_change=PricerBondState.set_y_axis,
                        ),
                    ),
                    rx.vstack(
                        rx.text("Z-Axis (3D)", font_size="0.8rem", weight="bold", color="blue"),
                        rx.select(
                            ["None", "Coupon", "Convexity"],
                            value=PricerBondState.z_axis,
                            on_change=PricerBondState.set_z_axis,
                        ),
                    ),
                    spacing="4",
                ),
                rx.divider(my="4"),

                # --- THE CHART ---
                # Key: Use rx.plotly with the state figure
                rx.box(
                    rx.plotly(
                        data=PricerBondState.figure,
                        style={"width": "100%", "height": "600px"}
                    ),
                    width="100%",
                    height="600px",
                ),
                width="100%",
            ),
            width="100%",
        ),
        class_name="flex flex-col w-full h-full bg-white p-4",
        on_mount=PricerBondState.on_mount, # Ensure graph loads on start
    )
