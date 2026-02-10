import reflex as rx
import plotly.graph_objects as go

from pmt_core.services.pricing import WarrantPricer


class PricerWarrantState(rx.State):
    """State for the Warrant Pricer view with full form bindings."""

    # Chart axis selections
    x_axis: str = "Spot Price"
    y_axis: str = "Value"
    z_axis: str = "None"  # Options: "None", "Time", "Volatility"

    # Input parameters - Terms
    valuation_date: str = "2023-10-27"
    effective_date: str = "2023-01-15"
    maturity_date: str = "2025-01-15"
    underlying: str = "7203.T"
    maturity_ticker: str = "7203W1"
    spot_price: float = 2450.0
    strike_price: float = 2500.0
    hit_fee_dec: float = 0.02
    currency: str = "JPY"
    hit_rate: float = 0.15
    interest_rate: float = 0.005

    def _get_pricer(self) -> WarrantPricer:
        """Get a WarrantPricer instance."""
        return WarrantPricer()

    @rx.var
    def fair_value(self) -> str:
        """Calculate fair value based on inputs. Delegates to core."""
        pricer = self._get_pricer()
        value = pricer.calculate_fair_value(self.spot_price, self.strike_price)
        return f"¥{value:,.2f}"

    @rx.var
    def delta(self) -> str:
        """Calculate delta based on inputs. Delegates to core."""
        pricer = self._get_pricer()
        d = pricer.calculate_delta(self.spot_price, self.strike_price)
        return f"{d:.2f}"

    @rx.var
    def is_in_the_money(self) -> bool:
        """Check if warrant is in the money. Delegates to core."""
        pricer = self._get_pricer()
        return pricer.is_in_the_money(self.spot_price, self.strike_price)

    @rx.var
    def chart(self) -> go.Figure:
        return self.generate_chart()

    def generate_chart(self) -> go.Figure:
        """Generate chart based on axis selections. Data from core, rendering here."""
        pricer = self._get_pricer()

        if self.z_axis == "None":
            # 2D Chart — get curve data from core
            curve = pricer.generate_payoff_curve(self.strike_price, self.y_axis)

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
            # 3D Surface — get surface data from core
            surface = pricer.generate_surface_data(
                self.strike_price, self.y_axis, self.z_axis
            )

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

    def set_maturity_ticker(self, value: str):
        self.maturity_ticker = value

    def set_spot_price(self, value: str):
        try:
            self.spot_price = float(value) if value else 0.0
        except ValueError:
            pass

    def set_strike_price(self, value: str):
        try:
            self.strike_price = float(value) if value else 0.0
        except ValueError:
            pass

    def set_hit_fee_dec(self, value: str):
        try:
            self.hit_fee_dec = float(value) if value else 0.0
        except ValueError:
            pass

    def set_currency(self, value: str):
        self.currency = value

    def set_hit_rate(self, value: str):
        try:
            self.hit_rate = float(value) if value else 0.0
        except ValueError:
            pass

    def set_interest_rate(self, value: str):
        try:
            self.interest_rate = float(value) if value else 0.0
        except ValueError:
            pass
