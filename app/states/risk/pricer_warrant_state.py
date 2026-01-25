import reflex as rx
import plotly.graph_objects as go
import numpy as np

class PricerWarrantState(rx.State):
    x_axis: str = "Spot Price"
    y_axis: str = "Value"
    z_axis: str = "None"

    @rx.var
    def chart(self) -> go.Figure:
        return self.generate_chart()

    def generate_chart(self) -> go.Figure:
        if self.z_axis == "None":
            # 2D Chart: Payoff diagram or Value vs Spot
            x_vals = np.linspace(80, 120, 100)

            if self.y_axis == "Value":
                 # Call option payoff-like shape + time value
                 y_vals = np.maximum(x_vals - 100, 0) + np.exp(-(x_vals-100)**2/100)*5
            else:
                 y_vals = np.random.normal(0, 1, 100).cumsum()

            fig = go.Figure(data=go.Scatter(x=x_vals, y=y_vals, mode='lines'))
            fig.update_layout(
                title=f"{self.y_axis} vs {self.x_axis}",
                xaxis_title=self.x_axis,
                yaxis_title=self.y_axis,
                template="plotly_white"
            )
            return fig
        else:
            # 3D Chart: Volatility Surface
            x = np.linspace(80, 120, 30) # Spot / Strike
            y = np.linspace(0.1, 2, 30)  # Time to maturity
            X, Y = np.meshgrid(x, y)

            # Black-Scholes-like surface shape mock
            Z = np.maximum(X - 100, 0) * np.exp(-0.05 * Y) + 5 * np.exp(-0.5 * ((X-100)/10)**2) * np.sqrt(Y)

            fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
            fig.update_layout(
                title=f"{self.y_axis} vs {self.x_axis} vs {self.z_axis}",
                scene=dict(
                    xaxis_title=self.x_axis,
                    yaxis_title=self.y_axis,
                    zaxis_title=self.z_axis
                ),
                template="plotly_white"
            )
            return fig
