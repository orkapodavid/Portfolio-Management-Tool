import reflex as rx
from app.states.risk.pricer_warrant_state import PricerWarrantState

# Design constants matching performance_header.py
POSITIVE_GREEN = "#00AA00"
NEGATIVE_RED = "#DD0000"


def header_cell(text: str, align: str = "left") -> rx.Component:
    """Table header cell helper."""
    return rx.el.th(
        text,
        class_name=f"px-3 py-3 text-{align} text-[10px] font-bold text-gray-700 uppercase tracking-widest border-b-2 border-gray-400 bg-[#E5E7EB] sticky top-0 z-30 shadow-sm h-[44px] whitespace-nowrap",
    )


def text_cell(val: str) -> rx.Component:
    """Table text cell helper."""
    return rx.el.td(
        val,
        class_name="px-3 py-2 text-[10px] font-medium text-gray-700 border-b border-gray-200 align-middle whitespace-nowrap",
    )


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


def pricer_warrant_view() -> rx.Component:
    return rx.el.div(
        # Top Section: Terms and Simulations
        rx.el.div(
            # Left Column: Terms Card with accent border
            rx.el.div(
                rx.el.h3(
                    "Terms",
                    class_name="text-[10px] font-black text-gray-600 uppercase tracking-[0.15em] mb-3 pb-2 border-b border-gray-200",
                ),
                rx.el.div(
                    # Date inputs
                    term_input(
                        "Valuation Date",
                        "date",
                        PricerWarrantState.valuation_date,
                        PricerWarrantState.set_valuation_date,
                    ),
                    term_input(
                        "Effective Date",
                        "date",
                        PricerWarrantState.effective_date,
                        PricerWarrantState.set_effective_date,
                    ),
                    term_input(
                        "Maturity Date",
                        "date",
                        PricerWarrantState.maturity_date,
                        PricerWarrantState.set_maturity_date,
                    ),
                    # Text inputs
                    term_input(
                        "Underlying",
                        "text",
                        PricerWarrantState.underlying,
                        PricerWarrantState.set_underlying,
                        placeholder="e.g. 7203.T",
                    ),
                    term_input(
                        "Maturity Ticker",
                        "text",
                        PricerWarrantState.maturity_ticker,
                        PricerWarrantState.set_maturity_ticker,
                        placeholder="e.g. 7203W1",
                    ),
                    # Numeric inputs
                    term_input(
                        "Spot Price",
                        "number",
                        PricerWarrantState.spot_price,
                        PricerWarrantState.set_spot_price,
                        placeholder="e.g. 2450",
                    ),
                    term_input(
                        "Strike Price",
                        "number",
                        PricerWarrantState.strike_price,
                        PricerWarrantState.set_strike_price,
                        placeholder="e.g. 2500",
                    ),
                    term_input(
                        "Hit Fee Dec",
                        "number",
                        PricerWarrantState.hit_fee_dec,
                        PricerWarrantState.set_hit_fee_dec,
                        placeholder="e.g. 0.02",
                    ),
                    term_input(
                        "Currency",
                        "text",
                        PricerWarrantState.currency,
                        PricerWarrantState.set_currency,
                        placeholder="e.g. JPY",
                    ),
                    term_input(
                        "Hit Rate",
                        "number",
                        PricerWarrantState.hit_rate,
                        PricerWarrantState.set_hit_rate,
                        placeholder="e.g. 0.15",
                    ),
                    term_input(
                        "Interest Rate",
                        "number",
                        PricerWarrantState.interest_rate,
                        PricerWarrantState.set_interest_rate,
                        placeholder="e.g. 0.005",
                    ),
                    class_name="grid grid-cols-2 gap-3 text-xs",
                ),
                class_name=f"w-1/3 p-4 border-l-[3px] border-[{POSITIVE_GREEN}] bg-white shadow-sm overflow-y-auto",
            ),
            # Right Column: Simulations & Outputs
            rx.el.div(
                rx.el.h3(
                    "Simulations & Outputs",
                    class_name="text-[10px] font-black text-gray-600 uppercase tracking-[0.15em] mb-3 pb-2 border-b border-gray-200",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                header_cell("Simulation#"), header_cell("Jump to 0")
                            )
                        ),
                        rx.el.tbody(rx.el.tr(text_cell("1"), text_cell("No"))),
                        class_name="w-full table-auto border-separate border-spacing-0 mb-4",
                    ),
                    # Key metrics with color coding
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                "Fair Value",
                                class_name="text-[8px] font-black text-gray-400 uppercase tracking-[0.1em] block",
                            ),
                            rx.el.span(
                                PricerWarrantState.fair_value,
                                class_name=rx.cond(
                                    PricerWarrantState.is_in_the_money,
                                    f"text-lg font-black text-[{POSITIVE_GREEN}] font-mono",
                                    f"text-lg font-black text-[{NEGATIVE_RED}] font-mono",
                                ),
                            ),
                            class_name="mb-3",
                        ),
                        rx.el.div(
                            rx.el.span(
                                "Delta",
                                class_name="text-[8px] font-black text-gray-400 uppercase tracking-[0.1em] block",
                            ),
                            rx.el.span(
                                PricerWarrantState.delta,
                                class_name="text-md font-bold text-gray-700 font-mono",
                            ),
                        ),
                        class_name=f"p-4 bg-gray-50 rounded border-l-[3px] border-[{POSITIVE_GREEN}] shadow-sm",
                    ),
                    class_name="flex flex-col gap-4",
                ),
                class_name="flex-1 p-4 bg-white",
            ),
            class_name="flex w-full bg-white border-b border-gray-200",
        ),
        # Middle Section: Visualization Controls
        rx.el.div(
            axis_control(
                "X-Axis",
                ["Spot Price", "Strike", "Volatility"],
                PricerWarrantState.x_axis,
                PricerWarrantState.set_x_axis,
            ),
            axis_control(
                "Y-Axis",
                ["Value", "Delta", "Gamma"],
                PricerWarrantState.y_axis,
                PricerWarrantState.set_y_axis,
            ),
            axis_control(
                "Z-Axis (3D)",
                ["None", "Time", "Volatility"],
                PricerWarrantState.z_axis,
                PricerWarrantState.set_z_axis,
                is_3d=True,
            ),
            class_name="flex gap-6 p-3 bg-gray-50 border-b border-gray-200 items-end",
        ),
        # Bottom Section: Chart
        rx.el.div(
            rx.plotly(
                data=PricerWarrantState.chart, style={"width": "100%", "height": "100%"}
            ),
            class_name="w-full flex-1 p-4 min-h-[600px]",
        ),
        class_name="flex flex-col w-full h-full bg-white",
    )
