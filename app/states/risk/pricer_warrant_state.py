"""
Pricer Warrant State — full form bindings for all Term, Simulation, and Output fields.

Outputs are computed on-demand via calculate() (triggered by the Calculate button),
not auto-computed on every keystroke.
"""

import reflex as rx
import plotly.graph_objects as go
from datetime import date

from pmt_core.services.pricing import WarrantPricer


class PricerWarrantState(rx.State):
    """State for the Warrant Pricer view with full form bindings."""

    # ── Chart axis selections ──────────────────────────────────────────
    x_axis: str = "Spot Price"
    y_axis: str = "Value"
    z_axis: str = "None"

    # ── TERMS ──────────────────────────────────────────────────────────
    # Dates
    valuation_date: str = "2026-02-10"
    effective_date: str = "2026-02-10"
    maturity_date: str = "2026-03-12"

    # Identifiers
    underlying: str = "7777 JP"
    model_ticker: str = "7777 JP Warrant"

    # Pricing inputs
    spot_price: str = "498"
    strike_price: str = "498"
    min_exe_disc: str = "0.0"
    currency: str = "JPY"
    fx_rate: str = "155.88"
    interest_rate: str = "0.0073"
    volatility: str = "0.3"
    borrow_rate_bps: str = "1000"

    # Reset fields
    reset_frequency: str = "(none)"
    reset_month: str = "(none)"
    reset_on_day: str = "1"
    reset_lookback_days: str = "10"
    reset_multiplier: str = "0.9"
    reset_cap_price: str = ""
    reset_floor_price: str = ""
    reset_up_down: str = "up and down"

    # ── SIMULATIONS ────────────────────────────────────────────────────
    seed: str = "0"
    trial_num: str = "5"
    simulation_num: str = "100"
    jump_lambda: str = "0"
    jump_mean: str = "0.0"
    jump_std_dev: str = "0.2"
    jump_to_zero: str = "False"

    # ── OUTPUTS (set by calculate()) ───────────────────────────────────
    result_fair_value: str = "JPY 15.5"
    result_delta: str = "0.47"
    result_expected_discount: str = "0.03%"

    # ── Helper ─────────────────────────────────────────────────────────
    def _get_pricer(self) -> WarrantPricer:
        return WarrantPricer()

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

        result = pricer.price_warrant(
            spot_price=self._safe_float(self.spot_price),
            strike_price=self._safe_float(self.strike_price),
            volatility=self._safe_float(self.volatility, 0.3),
            interest_rate=self._safe_float(self.interest_rate, 0.005),
            borrow_rate_bps=self._safe_int(self.borrow_rate_bps),
            time_to_maturity_years=ttm,
            min_exe_disc=self._safe_float(self.min_exe_disc),
            reset_lookback_days=self._safe_int(self.reset_lookback_days, 10),
            reset_multiplier=self._safe_float(self.reset_multiplier, 0.9),
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

    # ── Computed vars for chart ────────────────────────────────────────
    @rx.var
    def is_in_the_money(self) -> bool:
        pricer = self._get_pricer()
        return pricer.is_in_the_money(
            self._safe_float(self.spot_price),
            self._safe_float(self.strike_price),
        )

    @rx.var
    def chart(self) -> go.Figure:
        return self._generate_chart()

    def _generate_chart(self) -> go.Figure:
        pricer = self._get_pricer()
        sp = self._safe_float(self.strike_price, 100)

        if self.z_axis == "None":
            curve = pricer.generate_payoff_curve(sp, self.y_axis)
            fig = go.Figure(
                data=go.Scatter(
                    x=curve["x_values"],
                    y=curve["y_values"],
                    mode="lines",
                    line=dict(width=2),
                )
            )
            fig.update_layout(
                title=f"{self.y_axis} vs {self.x_axis}",
                xaxis_title=self.x_axis,
                yaxis_title=self.y_axis,
                template="plotly_white",
                height=600,
                margin=dict(l=20, r=20, t=50, b=20),
            )
            return fig
        else:
            surface = pricer.generate_surface_data(sp, self.y_axis, self.z_axis)
            fig = go.Figure(
                data=[
                    go.Surface(
                        z=surface["Z_grid"],
                        x=surface["X_grid"],
                        y=surface["Y_grid"],
                        colorscale=surface["colorscale"],
                    )
                ]
            )
            fig.update_layout(
                title=f"{self.z_axis} Surface ({self.x_axis} vs {self.y_axis})",
                scene=dict(
                    xaxis_title=self.x_axis,
                    yaxis_title=self.y_axis if self.y_axis != "Value" else "Time",
                    zaxis_title=self.z_axis,
                    aspectratio=dict(x=1, y=1, z=0.7),
                    camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
                ),
                template="plotly_white",
                height=600,
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

    def set_model_ticker(self, value: str):
        self.model_ticker = value

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
