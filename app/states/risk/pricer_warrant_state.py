import reflex as rx
import plotly.graph_objects as go
import numpy as np


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

    @rx.var
    def fair_value(self) -> str:
        """Calculate fair value based on inputs (mock calculation)."""
        intrinsic = max(0, self.spot_price - self.strike_price)
        time_value = self.spot_price * 0.05
        value = intrinsic + time_value
        return f"¥{value:,.2f}"

    @rx.var
    def delta(self) -> str:
        """Calculate delta based on inputs (mock calculation)."""
        moneyness = self.spot_price / self.strike_price if self.strike_price > 0 else 1
        if moneyness > 1.1:
            d = 0.85
        elif moneyness > 1.0:
            d = 0.65
        elif moneyness > 0.9:
            d = 0.45
        else:
            d = 0.25
        return f"{d:.2f}"

    @rx.var
    def is_in_the_money(self) -> bool:
        """Check if warrant is in the money."""
        return self.spot_price > self.strike_price

    @rx.var
    def chart(self) -> go.Figure:
        return self.generate_chart()

    def generate_chart(self) -> go.Figure:
        """Generate chart based on axis selections and input parameters."""
        # Use spot and strike from state for chart generation
        center = self.strike_price if self.strike_price > 0 else 100
        x_vals = np.linspace(center * 0.8, center * 1.2, 100)

        if self.z_axis == "None":
            # 2D Chart
            if self.y_axis == "Value":
                y_vals = np.maximum(x_vals - self.strike_price, 0) + np.exp(
                    -((x_vals - self.strike_price) ** 2) / (center * 10)
                ) * (center * 0.05)
            elif self.y_axis == "Delta":
                y_vals = 0.5 + 0.5 * np.tanh(
                    (x_vals - self.strike_price) / (center * 0.1)
                )
            else:  # Gamma
                y_vals = 0.01 * np.exp(
                    -(((x_vals - self.strike_price) / (center * 0.2)) ** 2)
                )

            fig = go.Figure(
                data=go.Scatter(x=x_vals, y=y_vals, mode="lines", line=dict(width=2))
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
            # 3D Surface Chart
            x = np.linspace(center * 0.8, center * 1.2, 50)
            y = (
                np.linspace(0.1, 2, 50)
                if self.y_axis == "Value"
                else np.linspace(0, 1, 50)
            )
            X, Y = np.meshgrid(x, y)

            if self.z_axis == "Volatility":
                Z = (
                    0.2
                    + 0.1 * ((X - self.strike_price) / center) ** 2
                    + 0.05 * np.exp(-Y)
                )
                colorscale = "Plasma"
            else:  # Time
                Z = np.maximum(X - self.strike_price, 0) * np.exp(-0.05 * Y) + (
                    center * 0.05
                ) * np.exp(
                    -0.5 * ((X - self.strike_price) / (center * 0.1)) ** 2
                ) * np.sqrt(Y)
                colorscale = "Viridis"

            fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale=colorscale)])
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
