import reflex as rx
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

from pmt_core.services.pricing import BondPricer


class PricerBondState(rx.State):
    # Selections
    x_axis: str = "Maturity"
    y_axis: str = "Yield"
    z_axis: str = "None"  # Options: "None", "Coupon", "Convexity"

    # Input parameters
    valuation_date: str = "2023-10-27"
    coupon_rate: float = 4.5

    # The Chart Figure
    figure: go.Figure = go.Figure()

    def _get_pricer(self) -> BondPricer:
        """Get a BondPricer instance with current parameters."""
        return BondPricer(coupon_rate=self.coupon_rate)

    def update_chart(self):
        """Regenerate the chart based on axes selection."""
        pricer = self._get_pricer()

        if self.z_axis == "None":
            # --- 2D SCENARIO ---
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
            self.figure = fig

        else:
            # --- 3D SCENARIO ---
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
            self.figure = fig

    def on_mount(self):
        """Initialize chart on load"""
        self.update_chart()

    def set_x_axis(self, value):
        self.x_axis = value
        self.update_chart()

    def set_y_axis(self, value):
        self.y_axis = value
        self.update_chart()

    def set_z_axis(self, value):
        self.z_axis = value
        self.update_chart()

    def set_valuation_date(self, value: str):
        self.valuation_date = value
        self.update_chart()

    def set_coupon_rate(self, value: str):
        try:
            self.coupon_rate = float(value) if value else 0.0
            self.update_chart()
        except ValueError:
            pass
