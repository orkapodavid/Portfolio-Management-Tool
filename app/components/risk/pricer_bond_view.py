import reflex as rx
from app.states.risk.pricer_bond_state import PricerBondState
from .risk_views import header_cell, text_cell

# Design constants matching performance_header.py
POSITIVE_GREEN = "#00AA00"
NEGATIVE_RED = "#DD0000"


def term_input(
    label: str, input_type: str, value, on_change, placeholder: str = ""
) -> rx.Component:
    """Styled input field with accent border matching performance_header pattern."""
    return rx.el.div(
        rx.el.label(
            label,
            class_name="text-[8px] font-black text-gray-400 uppercase tracking-[0.1em] block mb-1",
        ),
        rx.el.input(
            type=input_type,
            placeholder=placeholder,
            value=value,
            on_change=on_change,
            class_name="border border-gray-300 rounded p-1.5 w-full text-xs font-medium text-gray-800 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-colors",
        ),
        class_name="flex flex-col",
    )


def axis_control(
    label: str, options: list, value, on_change, is_3d: bool = False
) -> rx.Component:
    """Styled axis selector with proper label alignment."""
    label_class = (
        "text-[10px] font-bold text-blue-600"
        if is_3d
        else "text-[10px] font-bold text-gray-600"
    )
    return rx.el.div(
        rx.el.label(label, class_name=label_class),
        rx.select(
            options,
            value=value,
            on_change=on_change,
            size="1",
        ),
        class_name="flex flex-col gap-1",
    )


def pricer_bond_view() -> rx.Component:
    return rx.el.div(
        # Top Section: Terms and Pricing Results
        rx.el.div(
            # Left Column: Terms Card with accent border
            rx.el.div(
                rx.el.h3(
                    "Terms",
                    class_name="text-[10px] font-black text-gray-600 uppercase tracking-[0.15em] mb-3 pb-2 border-b border-gray-200",
                ),
                rx.el.div(
                    term_input(
                        "Valuation Date",
                        "date",
                        PricerBondState.valuation_date,
                        PricerBondState.set_valuation_date,
                    ),
                    term_input(
                        "Coupon Rate (%)",
                        "number",
                        PricerBondState.coupon_rate,
                        PricerBondState.set_coupon_rate,
                        placeholder="e.g. 4.5",
                    ),
                    class_name="grid grid-cols-1 gap-3 text-xs",
                ),
                class_name=f"w-1/4 p-4 border-l-[3px] border-[{POSITIVE_GREEN}] bg-white shadow-sm overflow-y-auto",
            ),
            # Right Column: Pricing Results
            rx.el.div(
                rx.el.h3(
                    "Pricing Results",
                    class_name="text-[10px] font-black text-gray-600 uppercase tracking-[0.15em] mb-3 pb-2 border-b border-gray-200",
                ),
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            header_cell("Ticker"),
                            header_cell("Spot Price", "right"),
                            header_cell("Fair Value", "right"),
                            header_cell("Discount", "right"),
                        )
                    ),
                    rx.el.tbody(
                        rx.el.tr(
                            text_cell("AAPL 4.5% 2029"),
                            rx.el.td(
                                "98.50",
                                class_name="px-3 py-2 text-[10px] font-mono font-medium text-gray-700 border-b border-gray-200 text-right",
                            ),
                            rx.el.td(
                                "99.25",
                                class_name="px-3 py-2 text-[10px] font-mono font-medium text-gray-700 border-b border-gray-200 text-right",
                            ),
                            rx.el.td(
                                "+0.75%",
                                class_name=f"px-3 py-2 text-[10px] font-mono font-bold text-[{POSITIVE_GREEN}] border-b border-gray-200 text-right",
                            ),
                            class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors",
                        ),
                        rx.el.tr(
                            text_cell("MSFT 3.0% 2028"),
                            rx.el.td(
                                "95.20",
                                class_name="px-3 py-2 text-[10px] font-mono font-medium text-gray-700 border-b border-gray-200 text-right",
                            ),
                            rx.el.td(
                                "94.80",
                                class_name="px-3 py-2 text-[10px] font-mono font-medium text-gray-700 border-b border-gray-200 text-right",
                            ),
                            rx.el.td(
                                "-0.42%",
                                class_name=f"px-3 py-2 text-[10px] font-mono font-bold text-[{NEGATIVE_RED}] border-b border-gray-200 text-right",
                            ),
                            class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors",
                        ),
                    ),
                    class_name="w-full table-auto border-separate border-spacing-0",
                ),
                class_name="flex-1 p-4 bg-white",
            ),
            class_name="flex w-full bg-white border-b border-gray-200",
        ),
        # Chart Controls Section
        rx.el.div(
            axis_control(
                "X-Axis",
                ["Maturity", "Duration"],
                PricerBondState.x_axis,
                PricerBondState.set_x_axis,
            ),
            axis_control(
                "Y-Axis",
                ["Yield", "Price"],
                PricerBondState.y_axis,
                PricerBondState.set_y_axis,
            ),
            axis_control(
                "Z-Axis (3D)",
                ["None", "Coupon", "Convexity"],
                PricerBondState.z_axis,
                PricerBondState.set_z_axis,
                is_3d=True,
            ),
            class_name="flex gap-6 p-3 bg-gray-50 border-b border-gray-200 items-end",
        ),
        # Chart Section
        rx.el.div(
            rx.plotly(
                data=PricerBondState.figure, style={"width": "100%", "height": "100%"}
            ),
            class_name="w-full flex-1 p-4 min-h-[600px]",
        ),
        class_name="flex flex-col w-full h-full bg-white",
        on_mount=PricerBondState.on_mount,
    )
