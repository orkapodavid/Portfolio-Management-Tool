"""
Pricer Bond View — Full financial-grade form interface.

Layout (three-panel):
  - Left panel (~25%): Terms (dates, identifiers, pricing inputs, reset group)
  - Middle panel (~25%): Terms Cont. + Simulations + Outputs (6 metrics)
  - Right panel (~50%): Data Grid (10 columns with mock CB data)
  - Footer: Notes section, "Generate Pricer Bond" button, Chart controls, Chart
"""

import reflex as rx
from app.states.risk.pricer_bond_state import PricerBondState

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
    """Left panel: Terms fields."""
    S = PricerBondState
    return rx.el.div(
        rx.el.h3("Terms", class_name=_SECTION_HEADER_CLS),
        # Identifiers row
        rx.el.div(
            _select_field("Model Instrument", ["7777 JP CB", "7203 JP CB", "9984 JP CB"], S.model_instrument, S.set_model_instrument),
            _field("Underlying", "text", S.underlying, S.set_underlying, "e.g. 7777 JP"),
            class_name="grid grid-cols-2 gap-3 mb-3",
        ),
        # Dates
        rx.el.div(
            _field("Valuation Date", "date", S.valuation_date, S.set_valuation_date),
            _field("Effective Date", "date", S.effective_date, S.set_effective_date),
            _field("Maturity Date", "date", S.maturity_date, S.set_maturity_date),
            class_name="grid grid-cols-3 gap-3 mb-3",
        ),
        # Core pricing fields
        rx.el.div(
            _field("Spot Price (Opt)", "text", S.spot_price, S.set_spot_price, "506"),
            _field("Strike Price", "text", S.strike_price, S.set_strike_price, "506"),
            _field("Min Exe Disc %", "text", S.min_exe_disc, S.set_min_exe_disc, "0.0"),
            _field("Currency", "text", S.currency, S.set_currency, "JPY"),
            _field("FX Rate (Opt)", "text", S.fx_rate, S.set_fx_rate, "155.88"),
            _field("Interest Rate (Opt)", "text", S.interest_rate, S.set_interest_rate, "0.0073"),
            _field("Volatility", "text", S.volatility, S.set_volatility, "0.3"),
            _field("Borrow Rate (bps)", "text", S.borrow_rate_bps, S.set_borrow_rate_bps, "1000"),
            _field("Credit Spread (bps)", "text", S.credit_spread_bps, S.set_credit_spread_bps, "3000"),
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
                _field("Reset Floor Price (Opt)", "text", S.reset_floor_price, S.set_reset_floor_price),
                _select_field("Reset Up/Down", ["up and down", "up only", "down only"], S.reset_up_down, S.set_reset_up_down),
                class_name="grid grid-cols-2 gap-x-4 gap-y-2",
            ),
            class_name="p-3 bg-blue-50/50 border border-blue-200 rounded-lg",
        ),
        class_name="flex-[3] p-4 bg-white overflow-y-auto",
    )


def _terms_cont_section() -> rx.Component:
    """Middle panel top: Bond-specific Terms Cont. fields."""
    S = PricerBondState
    return rx.el.div(
        rx.el.h3("Terms Cont.", class_name=_SECTION_HEADER_CLS),
        rx.el.div(
            _field("Notional", "text", S.notional, S.set_notional, "100"),
            _field("Exec/Redeemed", "text", S.exec_redeemed, S.set_exec_redeemed, "0"),
            _field("Coupon Rate", "text", S.coupon_rate, S.set_coupon_rate, "0.0"),
            _select_field("Coupon Freq", ["(none)", "semi-annual", "annual", "quarterly"], S.coupon_freq, S.set_coupon_freq),
            _field("Redemption Rate", "text", S.redemption_rate, S.set_redemption_rate, "1.0"),
            _select_field("Redemption Freq", ["(none)", "annual", "semi-annual", "quarterly"], S.redemption_freq, S.set_redemption_freq),
            _select_field("Redemption Deferral", ["(none)", "30 days", "60 days", "90 days"], S.redemption_deferral, S.set_redemption_deferral),
            _select_field("Redemption Date Only", ["(none)", "True", "False"], S.redemption_date_only, S.set_redemption_date_only),
            class_name="grid grid-cols-2 gap-x-4 gap-y-2",
        ),
        class_name="p-4 bg-white",
    )


def _simulations_section() -> rx.Component:
    """Middle panel middle: 7 Simulation fields."""
    S = PricerBondState
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
        class_name="p-4 bg-white border-t border-gray-200",
    )


def _outputs_section() -> rx.Component:
    """Middle panel bottom: 6 read-only output metrics."""
    S = PricerBondState
    return rx.el.div(
        rx.el.h3("Outputs", class_name=_SECTION_HEADER_CLS),
        rx.el.div(
            _output_metric("Fair Value", S.result_fair_value, accent=True),
            _output_metric("Delta", S.result_delta),
            _output_metric("Exp. Discount", S.result_expected_discount),
            _output_metric("Bond Delta", S.result_bond_delta),
            _output_metric("Bond Floor", S.result_bond_floor),
            _output_metric("Bond Parity", S.result_bond_parity),
            class_name="grid grid-cols-3 gap-4 mb-4",
        ),
        class_name="p-4 bg-gray-50 border-t border-gray-200",
    )


# ── Data Grid section ────────────────────────────────────────────────

def _header_cell(text: str, align: str = "left") -> rx.Component:
    """Table header cell."""
    return rx.el.th(
        text,
        class_name=f"px-3 py-3 text-{align} text-[10px] font-bold text-gray-700 uppercase tracking-widest border-b-2 border-gray-400 bg-[#E5E7EB] sticky top-0 z-30 shadow-sm h-[44px] whitespace-nowrap",
    )


def _text_cell(val: str) -> rx.Component:
    """Text cell."""
    return rx.el.td(
        val,
        class_name="px-3 py-2 text-[10px] font-medium text-gray-700 border-b border-gray-200 align-middle whitespace-nowrap",
    )


def _num_cell(val: str, color: str = "") -> rx.Component:
    """Numeric right-aligned cell."""
    if color:
        cls = f"px-3 py-2 text-[10px] font-mono font-bold text-[{color}] border-b border-gray-200 text-right"
    else:
        cls = "px-3 py-2 text-[10px] font-mono font-medium text-gray-700 border-b border-gray-200 text-right"
    return rx.el.td(val, class_name=cls)


def _data_grid_section() -> rx.Component:
    """Right panel: large results data grid with 10 columns."""
    # Mock CB pricing data
    rows = [
        ("7777 JP CB", "¥506.000", "¥101.020", "0.00%", "", "JPY", "2026-02-11", "¥506.000", "¥100.000", "0.14", "¥97.508"),
        ("7777 JP CB", "¥504.710", "¥101.020", "(0.24%)", NEGATIVE_RED, "JPY", "2026-01-25", "¥506.000", "¥99.745", "0.14", "¥97.508"),
        ("7777 JP CB", "¥504.211", "¥100.121", "(0.12%)", NEGATIVE_RED, "JPY", "2026-02-05", "¥506.000", "¥99.646", "0.14", "¥97.500"),
        ("7777 JP CB", "¥503.500", "¥100.050", "0.05%", "", "JPY", "2026-02-10", "¥506.000", "¥99.505", "0.13", "¥97.250"),
        ("7777 JP CB", "¥507.100", "¥101.420", "0.42%", "", "JPY", "2026-02-11", "¥506.000", "¥100.217", "0.14", "¥97.650"),
        ("7777 JP CB", "¥500.000", "¥99.800", "(0.20%)", NEGATIVE_RED, "JPY", "2026-01-15", "¥506.000", "¥98.814", "0.12", "¥97.000"),
    ]

    return rx.el.div(
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        _header_cell("Ticker"),
                        _header_cell("Spot Price", "right"),
                        _header_cell("Fair Value", "right"),
                        _header_cell("Discount", "right"),
                        _header_cell("Currency"),
                        _header_cell("Trade Date"),
                        _header_cell("Strike Price", "right"),
                        _header_cell("Parity", "right"),
                        _header_cell("Delta", "right"),
                        _header_cell("Bond Floor", "right"),
                    )
                ),
                rx.el.tbody(
                    *[
                        rx.el.tr(
                            _text_cell(ticker),
                            _num_cell(spot),
                            _num_cell(fv),
                            _num_cell(disc, color) if color else _num_cell(disc),
                            _text_cell(ccy),
                            _text_cell(trade_dt),
                            _num_cell(strike),
                            _num_cell(parity),
                            _num_cell(delta),
                            _num_cell(bf),
                            class_name="odd:bg-white even:bg-gray-50 hover:bg-gray-100 transition-colors",
                        )
                        for ticker, spot, fv, disc, color, ccy, trade_dt, strike, parity, delta, bf in rows
                    ],
                ),
                class_name="w-full table-auto border-separate border-spacing-0",
            ),
            class_name="overflow-x-auto",
        ),
        class_name="p-4 bg-white flex-1",
    )


# ── Notes section ────────────────────────────────────────────────────

def _notes_section() -> rx.Component:
    """Validation rules for bond pricer."""
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
        ),
        class_name="px-4 py-3 bg-amber-50/50 border border-amber-200/60 rounded-lg",
    )


# ── Chart controls ───────────────────────────────────────────────────

def _chart_controls() -> rx.Component:
    """Axis selectors for the chart."""
    S = PricerBondState

    def _axis(label: str, options: list, value, on_change, is_3d: bool = False):
        label_cls = "text-[10px] font-bold text-blue-600" if is_3d else "text-[10px] font-bold text-gray-600"
        return rx.el.div(
            rx.el.label(label, class_name=label_cls),
            rx.select(options, value=value, on_change=on_change, size="1"),
            class_name="flex flex-col gap-1",
        )

    return rx.el.div(
        _axis("X-Axis", ["Maturity", "Duration"], S.x_axis, S.set_x_axis),
        _axis("Y-Axis", ["Yield", "Price"], S.y_axis, S.set_y_axis),
        _axis("Z-Axis (3D)", ["None", "Coupon", "Convexity"], S.z_axis, S.set_z_axis, is_3d=True),
        class_name="flex gap-6 p-3 bg-gray-50 border-b border-gray-200 items-end",
    )


# ── Main view ────────────────────────────────────────────────────────

def pricer_bond_view() -> rx.Component:
    return rx.el.div(
        # Three-panel layout: Terms | Terms Cont.+Simulations+Outputs | Data Grid
        rx.el.div(
            # Left panel: Terms
            _terms_section(),
            # Middle panel: Terms Cont. + Simulations + Outputs
            rx.el.div(
                _terms_cont_section(),
                _simulations_section(),
                _outputs_section(),
                class_name="flex-[3] flex flex-col border-l border-gray-200",
            ),
            # Right panel: Data Grid
            rx.el.div(
                _data_grid_section(),
                class_name="flex-[4] flex flex-col border-l border-gray-200",
            ),
            class_name="flex w-full bg-white border-b border-gray-200",
        ),
        # Notes section
        rx.el.div(
            _notes_section(),
            class_name="p-3",
        ),
        # Generate Pricer Bond button
        rx.el.div(
            rx.el.button(
                rx.icon("calculator", size=14),
                rx.el.span("Generate Pricer Bond", class_name="text-xs font-bold"),
                on_click=PricerBondState.calculate,
                class_name=(
                    "flex items-center justify-center gap-2 px-8 h-9 "
                    f"bg-[{ACCENT_BLUE}] hover:bg-blue-700 text-white "
                    "rounded-lg font-bold transition-colors shadow-md"
                ),
            ),
            class_name="flex justify-center py-3 border-b border-gray-200",
        ),
        # Chart controls
        _chart_controls(),
        # Chart
        rx.el.div(
            rx.plotly(
                data=PricerBondState.chart,
                style={"width": "100%", "height": "100%"},
            ),
            class_name="w-full flex-1 p-4 min-h-[600px]",
        ),
        class_name="flex flex-col w-full h-full bg-white",
    )
