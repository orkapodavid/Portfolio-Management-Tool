"""
Pricer Bond State — full form bindings for all Term, Terms Cont.,
Simulation, and Output fields.

Outputs are computed on-demand via calculate() (triggered by the
"Generate Pricer Bond" button), not auto-computed on every keystroke.
"""

import reflex as rx
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import date

from pmt_core.services.pricing import BondPricer


class PricerBondState(rx.State):
    """State for the Bond Pricer view with full form bindings."""

    # ── Chart axis selections ──────────────────────────────────────────
    x_axis: str = "Maturity"
    y_axis: str = "Yield"
    z_axis: str = "None"

    # ── TERMS ──────────────────────────────────────────────────────────
    # Dates
    valuation_date: str = "2026-02-11"
    effective_date: str = "2026-02-11"
    maturity_date: str = "2026-03-13"

    # Identifiers
    underlying: str = "7777 JP"
    model_instrument: str = "7777 JP CB"

    # Pricing inputs
    spot_price: str = "506"
    strike_price: str = "506"
    min_exe_disc: str = "0.0"
    currency: str = "JPY"
    fx_rate: str = "155.88"
    interest_rate: str = "0.0073"
    volatility: str = "0.3"
    borrow_rate_bps: str = "1000"
    credit_spread_bps: str = "3000"

    # Reset fields
    reset_frequency: str = "(none)"
    reset_month: str = "(none)"
    reset_on_day: str = "1"
    reset_lookback_days: str = "10"
    reset_multiplier: str = "0.9"
    reset_cap_price: str = ""
    reset_floor_price: str = ""
    reset_up_down: str = "up and down"

    # ── TERMS CONT. (bond-specific) ────────────────────────────────────
    notional: str = "100"
    exec_redeemed: str = "0"
    coupon_rate: str = "0.0"
    coupon_freq: str = "(none)"
    redemption_rate: str = "1.0"
    redemption_freq: str = "(none)"
    redemption_deferral: str = "(none)"
    redemption_date_only: str = "(none)"

    # ── SIMULATIONS ────────────────────────────────────────────────────
    seed: str = "0"
    trial_num: str = "5"
    simulation_num: str = "100"
    jump_lambda: str = "0"
    jump_mean: str = "0.0"
    jump_std_dev: str = "0.2"
    jump_to_zero: str = "False"

    # ── OUTPUTS (set by calculate()) ───────────────────────────────────
    result_fair_value: str = "JPY 101.02"
    result_delta: str = "0.136"
    result_expected_discount: str = "0.03%"
    result_bond_delta: str = "0.686"
    result_bond_floor: str = "JPY 97.508"
    result_bond_parity: str = "JPY 100"

    # ── Helpers ─────────────────────────────────────────────────────────
    def _get_pricer(self) -> BondPricer:
        return BondPricer(coupon_rate=self._safe_float(self.coupon_rate, 4.5))

    def _safe_float(self, v: str, default: float = 0.0) -> float:
        try:
            return float(v) if v else default
        except ValueError:
            return default

    def _safe_int(self, v: str, default: int = 0) -> int:
        try:
            return int(v) if v else default
        except ValueError:
            return default

    # ── Calculate (manual trigger) ─────────────────────────────────────
    def calculate(self):
        """Run full pricing calculation and update outputs."""
        pricer = self._get_pricer()

        # Compute time to maturity from dates
        try:
            val_date = date.fromisoformat(self.valuation_date)
            mat_date = date.fromisoformat(self.maturity_date)
            ttm = max((mat_date - val_date).days / 365.25, 0.001)
        except (ValueError, TypeError):
            ttm = 1.0

        result = pricer.price_bond(
            spot_price=self._safe_float(self.spot_price),
            strike_price=self._safe_float(self.strike_price),
            notional=self._safe_float(self.notional, 100.0),
            coupon_rate=self._safe_float(self.coupon_rate),
            redemption_rate=self._safe_float(self.redemption_rate, 1.0),
            volatility=self._safe_float(self.volatility, 0.3),
            interest_rate=self._safe_float(self.interest_rate, 0.005),
            borrow_rate_bps=self._safe_int(self.borrow_rate_bps),
            credit_spread_bps=self._safe_int(self.credit_spread_bps),
            time_to_maturity_years=ttm,
            min_exe_disc=self._safe_float(self.min_exe_disc),
            exec_redeemed=self._safe_int(self.exec_redeemed),
            seed=self._safe_int(self.seed),
            trial_num=self._safe_int(self.trial_num, 5),
            simulation_num=self._safe_int(self.simulation_num, 100),
            jump_lambda=self._safe_float(self.jump_lambda),
            jump_mean=self._safe_float(self.jump_mean),
            jump_std_dev=self._safe_float(self.jump_std_dev, 0.2),
            currency=self.currency,
        )

        self.result_fair_value = f"{result['currency']} {result['fair_value']}"
        self.result_delta = f"{result['delta']}"
        self.result_expected_discount = f"{result['expected_discount']}%"
        self.result_bond_delta = f"{result['bond_delta']}"
        self.result_bond_floor = f"{result['currency']} {result['bond_floor']}"
        self.result_bond_parity = f"{result['currency']} {result['bond_parity']}"

    # ── Computed vars for chart ────────────────────────────────────────
    @rx.var
    def chart(self) -> go.Figure:
        return self._generate_chart()

    def _generate_chart(self) -> go.Figure:
        pricer = self._get_pricer()

        if self.z_axis == "None":
            curve_data = pricer.generate_curve_data(self.x_axis, self.y_axis)
            df = pd.DataFrame({
                curve_data["x_label"]: curve_data["x_values"],
                curve_data["y_label"]: curve_data["y_values"],
            })
            fig = px.line(
                df,
                x=curve_data["x_label"],
                y=curve_data["y_label"],
                title=f"{curve_data['y_label']} vs {curve_data['x_label']}",
                markers=True,
            )
            fig.update_layout(
                template="plotly_white",
                height=500,
                margin=dict(l=20, r=20, t=50, b=20),
            )
            return fig
        else:
            surface = pricer.generate_surface_data(self.z_axis)
            fig = go.Figure(
                data=[
                    go.Surface(
                        x=surface["X_grid"],
                        y=surface["Y_grid"],
                        z=surface["Z_grid"],
                        colorscale=surface["colorscale"],
                        colorbar=dict(title=self.z_axis),
                    )
                ]
            )
            fig.update_layout(
                title=f"3D Surface: {self.z_axis} Analysis",
                autosize=True,
                height=600,
                scene=dict(
                    xaxis_title=self.x_axis,
                    yaxis_title=self.y_axis,
                    zaxis_title=self.z_axis,
                    aspectratio=dict(x=1, y=1, z=0.7),
                    camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
                ),
                margin=dict(l=10, r=10, t=50, b=10),
            )
            return fig

    # ── Setters ────────────────────────────────────────────────────────
    def set_x_axis(self, value: str):
        self.x_axis = value

    def set_y_axis(self, value: str):
        self.y_axis = value

    def set_z_axis(self, value: str):
        self.z_axis = value

    def set_valuation_date(self, value: str):
        self.valuation_date = value

    def set_effective_date(self, value: str):
        self.effective_date = value

    def set_maturity_date(self, value: str):
        self.maturity_date = value

    def set_underlying(self, value: str):
        self.underlying = value

    def set_model_instrument(self, value: str):
        self.model_instrument = value

    def set_spot_price(self, value: str):
        self.spot_price = value

    def set_strike_price(self, value: str):
        self.strike_price = value

    def set_min_exe_disc(self, value: str):
        self.min_exe_disc = value

    def set_currency(self, value: str):
        self.currency = value

    def set_fx_rate(self, value: str):
        self.fx_rate = value

    def set_interest_rate(self, value: str):
        self.interest_rate = value

    def set_volatility(self, value: str):
        self.volatility = value

    def set_borrow_rate_bps(self, value: str):
        self.borrow_rate_bps = value

    def set_credit_spread_bps(self, value: str):
        self.credit_spread_bps = value

    def set_reset_frequency(self, value: str):
        self.reset_frequency = value

    def set_reset_month(self, value: str):
        self.reset_month = value

    def set_reset_on_day(self, value: str):
        self.reset_on_day = value

    def set_reset_lookback_days(self, value: str):
        self.reset_lookback_days = value

    def set_reset_multiplier(self, value: str):
        self.reset_multiplier = value

    def set_reset_cap_price(self, value: str):
        self.reset_cap_price = value

    def set_reset_floor_price(self, value: str):
        self.reset_floor_price = value

    def set_reset_up_down(self, value: str):
        self.reset_up_down = value

    # Terms Cont. setters
    def set_notional(self, value: str):
        self.notional = value

    def set_exec_redeemed(self, value: str):
        self.exec_redeemed = value

    def set_coupon_rate(self, value: str):
        self.coupon_rate = value

    def set_coupon_freq(self, value: str):
        self.coupon_freq = value

    def set_redemption_rate(self, value: str):
        self.redemption_rate = value

    def set_redemption_freq(self, value: str):
        self.redemption_freq = value

    def set_redemption_deferral(self, value: str):
        self.redemption_deferral = value

    def set_redemption_date_only(self, value: str):
        self.redemption_date_only = value

    # Simulation setters
    def set_seed(self, value: str):
        self.seed = value

    def set_trial_num(self, value: str):
        self.trial_num = value

    def set_simulation_num(self, value: str):
        self.simulation_num = value

    def set_jump_lambda(self, value: str):
        self.jump_lambda = value

    def set_jump_mean(self, value: str):
        self.jump_mean = value

    def set_jump_std_dev(self, value: str):
        self.jump_std_dev = value

    def set_jump_to_zero(self, value: str):
        self.jump_to_zero = value
