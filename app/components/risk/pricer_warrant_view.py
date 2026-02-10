"""
Pricer Warrant View — Full financial-grade form interface.

Layout:
  - Left column (60%): Terms (21 fields, Reset fields in sub-group)
  - Right column (40%): Simulations (7 fields) + Outputs (3 read-only) + Calculate
  - Bottom: Notes section, Chart controls, Chart
"""

import reflex as rx
from app.states.risk.pricer_warrant_state import PricerWarrantState

# Design constants
POSITIVE_GREEN = "#00AA00"
NEGATIVE_RED = "#DD0000"
ACCENT_BLUE = "#2563EB"

# ── Shared component helpers ─────────────────────────────────────────

_LABEL_CLS = "text-[9px] font-bold text-gray-500 uppercase tracking-[0.08em] mb-0.5 block"
_INPUT_CLS = (
    "h-7 w-full px-2 text-[11px] font-medium text-gray-800 bg-white "
    "border border-gray-300 rounded focus:border-blue-500 focus:ring-1 "
    "focus:ring-blue-500 transition-colors [appearance:textfield] "
    "[&::-webkit-outer-spin-button]:appearance-none "
    "[&::-webkit-inner-spin-button]:appearance-none"
)
_SECTION_HEADER_CLS = (
    "text-[10px] font-black text-gray-600 uppercase tracking-[0.15em] "
    "mb-3 pb-2 border-b-2 border-gray-300"
)


def _field(label: str, input_type: str, value, on_change, placeholder: str = "") -> rx.Component:
    """Compact labeled input field."""
    return rx.el.div(
        rx.el.label(label, class_name=_LABEL_CLS),
        rx.el.input(
            type=input_type,
            value=value,
            on_change=on_change,
            placeholder=placeholder,
            class_name=_INPUT_CLS,
        ),
        class_name="flex flex-col",
    )


def _select_field(label: str, options: list[str], value, on_change) -> rx.Component:
    """Compact labeled dropdown."""
    return rx.el.div(
        rx.el.label(label, class_name=_LABEL_CLS),
        rx.select(
            options,
            value=value,
            on_change=on_change,
            size="1",
        ),
        class_name="flex flex-col gap-0.5",
    )


def _output_metric(label: str, value, accent: bool = False) -> rx.Component:
    """Read-only output display with label."""
    val_cls = (
        f"text-base font-black font-mono text-[{POSITIVE_GREEN}]"
        if accent
        else "text-base font-bold font-mono text-gray-700"
    )
    return rx.el.div(
        rx.el.span(label, class_name="text-[8px] font-bold text-gray-400 uppercase tracking-[0.1em] block mb-0.5"),
        rx.el.span(value, class_name=val_cls),
        class_name="",
    )


# ── Section builders ─────────────────────────────────────────────────

def _terms_section() -> rx.Component:
    """Left column: all 21 Term fields."""
    S = PricerWarrantState
    return rx.el.div(
        rx.el.h3("Terms", class_name=_SECTION_HEADER_CLS),
        # Date fields
        rx.el.div(
            _field("Valuation Date", "date", S.valuation_date, S.set_valuation_date),
            _field("Effective Date", "date", S.effective_date, S.set_effective_date),
            _field("Maturity Date", "date", S.maturity_date, S.set_maturity_date),
            class_name="grid grid-cols-3 gap-3 mb-3",
        ),
        # Core fields
        rx.el.div(
            _field("Underlying", "text", S.underlying, S.set_underlying, "e.g. 7777 JP"),
            _select_field("Model Ticker", ["7777 JP Warrant", "7203 JP Warrant", "9984 JP Warrant"], S.model_ticker, S.set_model_ticker),
            _field("Spot Price (Opt)", "text", S.spot_price, S.set_spot_price, "498"),
            _field("Strike Price", "text", S.strike_price, S.set_strike_price, "498"),
            _field("Min Exe Disc", "text", S.min_exe_disc, S.set_min_exe_disc, "0.0"),
            _field("Currency", "text", S.currency, S.set_currency, "JPY"),
            _field("FX Rate (Opt)", "text", S.fx_rate, S.set_fx_rate, "155.88"),
            _field("Interest Rate (Opt)", "text", S.interest_rate, S.set_interest_rate, "0.0073"),
            _field("Volatility", "text", S.volatility, S.set_volatility, "0.3"),
            _field("Borrow Rate (bps)", "text", S.borrow_rate_bps, S.set_borrow_rate_bps, "1000"),
            class_name="grid grid-cols-2 gap-x-4 gap-y-2 mb-4",
        ),
        # Reset fields — visually grouped
        rx.el.div(
            rx.el.h4(
                "Reset Parameters",
                class_name="text-[9px] font-black text-blue-600 uppercase tracking-[0.1em] mb-2",
            ),
            rx.el.div(
                _select_field("Reset Frequency", ["(none)", "daily", "weekly", "biweekly", "monthly", "quarterly"], S.reset_frequency, S.set_reset_frequency),
                _select_field("Reset Month", ["(none)", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"], S.reset_month, S.set_reset_month),
                _select_field("Reset on Day", ["1", "2", "3", "4", "5", "10", "15", "20", "25"], S.reset_on_day, S.set_reset_on_day),
                _field("Reset Lookback Days", "text", S.reset_lookback_days, S.set_reset_lookback_days, "10"),
                _field("Reset Multiplier", "text", S.reset_multiplier, S.set_reset_multiplier, "0.9"),
                _field("Reset Cap Price", "text", S.reset_cap_price, S.set_reset_cap_price),
                _field("Reset Floor Price", "text", S.reset_floor_price, S.set_reset_floor_price),
                _select_field("Reset Up/Down", ["up and down", "up only", "down only"], S.reset_up_down, S.set_reset_up_down),
                class_name="grid grid-cols-2 gap-x-4 gap-y-2",
            ),
            class_name="p-3 bg-blue-50/50 border border-blue-200 rounded-lg",
        ),
        class_name="flex-[3] p-4 bg-white",
    )


def _simulations_section() -> rx.Component:
    """Right column top: 7 Simulation fields."""
    S = PricerWarrantState
    return rx.el.div(
        rx.el.h3("Simulations", class_name=_SECTION_HEADER_CLS),
        rx.el.div(
            _field("Seed", "text", S.seed, S.set_seed, "0"),
            _field("Trial #", "text", S.trial_num, S.set_trial_num, "5"),
            _field("Simulation #", "text", S.simulation_num, S.set_simulation_num, "100"),
            _field("Jump Lambda", "text", S.jump_lambda, S.set_jump_lambda, "0"),
            _field("Jump Mean", "text", S.jump_mean, S.set_jump_mean, "0.0"),
            _field("Jump Std Dev", "text", S.jump_std_dev, S.set_jump_std_dev, "0.2"),
            _select_field("Jump to 0", ["False", "True"], S.jump_to_zero, S.set_jump_to_zero),
            class_name="grid grid-cols-2 gap-x-4 gap-y-2",
        ),
        class_name="p-4 bg-white",
    )


def _outputs_section() -> rx.Component:
    """Right column bottom: 3 read-only output metrics + Calculate button."""
    S = PricerWarrantState
    return rx.el.div(
        rx.el.h3("Outputs", class_name=_SECTION_HEADER_CLS),
        rx.el.div(
            _output_metric("Fair Value", S.result_fair_value, accent=True),
            _output_metric("Delta", S.result_delta),
            _output_metric("Expected Discount", S.result_expected_discount),
            class_name="grid grid-cols-3 gap-4 mb-4",
        ),
        rx.el.button(
            rx.icon("calculator", size=14),
            rx.el.span("Calculate", class_name="text-xs font-bold"),
            on_click=S.calculate,
            class_name=(
                "flex items-center justify-center gap-2 w-full h-9 "
                f"bg-[{ACCENT_BLUE}] hover:bg-blue-700 text-white "
                "rounded-lg font-bold transition-colors shadow-md"
            ),
        ),
        class_name=f"p-4 bg-gray-50 border-t border-gray-200",
    )


def _notes_section() -> rx.Component:
    """Collapsible notes section with validation rules."""
    notes = [
        "Field 'Model Ticker' is compulsory when 'Use Historical Spot' is True. Field 'Spot Price' is compulsory when 'Use Historical Spot' is False.",
        "Field 'Reset on Day' is compulsory if 'Reset Frequency' is greater than 'biweekly', and is unnecessary if 'Reset Frequency' is 'weekly' or 'biweekly'.",
        "Field 'Market Price Formula' has a format func([period]). [period] has a format 'd/m/y', 'x d/m/y' for x day or 'x wk d/m/y' for x week.",
        "Field 'Reset Price Formula' has a format func([x]). [x] is a fixed value that represents the market price. If field is empty, then reset price will be the executable price.",
        "Field 'Lookback Days' and 'Reset Multiplier' is compulsory when field 'Market Price Formula' is empty. Field 'Lookback Days' will start with the immediately preceding day.",
        "Field 'Interest Rate Ticker' or 'Interest Rate' should be set.",
        "Field 'Reset Cap' or 'Reset Floor Price' is optional.",
        "For formula can use any standard functions in python, numpy or pandas library.",
    ]
    return rx.el.div(
        rx.el.h4(
            rx.icon("info", size=12, class_name="text-amber-500"),
            rx.el.span("Notes", class_name="ml-1"),
            class_name="flex items-center text-[9px] font-black text-gray-500 uppercase tracking-[0.1em] mb-2",
        ),
        rx.el.div(
            *[
                rx.el.p(
                    f"• {note}",
                    class_name="text-[9px] text-gray-500 leading-relaxed mb-1",
                )
                for note in notes
            ],
            class_name="",
        ),
        class_name="px-4 py-3 bg-amber-50/50 border border-amber-200/60 rounded-lg",
    )


def _chart_controls() -> rx.Component:
    """Axis selectors for the chart."""
    S = PricerWarrantState

    def _axis(label: str, options: list, value, on_change, is_3d: bool = False):
        label_cls = "text-[10px] font-bold text-blue-600" if is_3d else "text-[10px] font-bold text-gray-600"
        return rx.el.div(
            rx.el.label(label, class_name=label_cls),
            rx.select(options, value=value, on_change=on_change, size="1"),
            class_name="flex flex-col gap-1",
        )

    return rx.el.div(
        _axis("X-Axis", ["Spot Price", "Strike", "Volatility"], S.x_axis, S.set_x_axis),
        _axis("Y-Axis", ["Value", "Delta", "Gamma"], S.y_axis, S.set_y_axis),
        _axis("Z-Axis (3D)", ["None", "Time", "Volatility"], S.z_axis, S.set_z_axis, is_3d=True),
        class_name="flex gap-6 p-3 bg-gray-50 border-b border-gray-200 items-end",
    )


# ── Main view ────────────────────────────────────────────────────────

def _header_cell(text: str, align: str = "left") -> rx.Component:
    """Table header cell helper."""
    return rx.el.th(
        text,
        class_name=f"px-3 py-3 text-{align} text-[10px] font-bold text-gray-700 uppercase tracking-widest border-b-2 border-gray-400 bg-[#E5E7EB] sticky top-0 z-30 shadow-sm h-[44px] whitespace-nowrap",
    )


def _text_cell(val: str) -> rx.Component:
    """Table text cell helper."""
    return rx.el.td(
        val,
        class_name="px-3 py-2 text-[10px] font-medium text-gray-700 border-b border-gray-200 align-middle whitespace-nowrap",
    )


def _num_cell(val: str, color: str = "") -> rx.Component:
    """Numeric right-aligned table cell."""
    cls = f"px-3 py-2 text-[10px] font-mono font-medium border-b border-gray-200 text-right"
    if color:
        cls = f"px-3 py-2 text-[10px] font-mono font-bold text-[{color}] border-b border-gray-200 text-right"
    else:
        cls = f"px-3 py-2 text-[10px] font-mono font-medium text-gray-700 border-b border-gray-200 text-right"
    return rx.el.td(val, class_name=cls)


def _pricing_results_section() -> rx.Component:
    """Pricing Results table matching the bond pricer pattern."""
    return rx.el.div(
        rx.el.h3(
            "Pricing Results",
            class_name=_SECTION_HEADER_CLS,
        ),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    _header_cell("Ticker"),
                    _header_cell("Spot Price", "right"),
                    _header_cell("Fair Value", "right"),
                    _header_cell("Discount", "right"),
                )
            ),
            rx.el.tbody(
                rx.el.tr(
                    _text_cell("7777 JP Warrant"),
                    _num_cell("498.00"),
                    _num_cell("15.50"),
                    _num_cell("+3.11%", POSITIVE_GREEN),
                    class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors",
                ),
                rx.el.tr(
                    _text_cell("7203 JP Warrant"),
                    _num_cell("2,845.00"),
                    _num_cell("142.25"),
                    _num_cell("+5.00%", POSITIVE_GREEN),
                    class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors",
                ),
                rx.el.tr(
                    _text_cell("9984 JP Warrant"),
                    _num_cell("8,520.00"),
                    _num_cell("380.10"),
                    _num_cell("-1.25%", NEGATIVE_RED),
                    class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors",
                ),
            ),
            class_name="w-full table-auto border-separate border-spacing-0",
        ),
        class_name="p-4 bg-white border-b border-gray-200",
    )


def pricer_warrant_view() -> rx.Component:
    return rx.el.div(
        # Three-column layout: Terms | Simulations+Outputs | Pricing Results
        rx.el.div(
            # Left column: Terms
            _terms_section(),
            # Middle column: Simulations + Outputs
            rx.el.div(
                _simulations_section(),
                _outputs_section(),
                class_name="flex-[2] flex flex-col border-l border-gray-200",
            ),
            # Right column: Pricing Results
            rx.el.div(
                _pricing_results_section(),
                class_name="flex-[2] flex flex-col border-l border-gray-200",
            ),
            class_name="flex w-full bg-white border-b border-gray-200",
        ),
        # Notes section
        rx.el.div(
            _notes_section(),
            class_name="p-3",
        ),
        # Chart controls
        _chart_controls(),
        # Chart
        rx.el.div(
            rx.plotly(
                data=PricerWarrantState.chart,
                style={"width": "100%", "height": "100%"},
            ),
            class_name="w-full flex-1 p-4 min-h-[600px]",
        ),
        class_name="flex flex-col w-full h-full bg-white",
    )
