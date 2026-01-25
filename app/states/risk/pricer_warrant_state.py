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
            # Using go.Surface requires a grid

            # X: Spot Price / Strike
            x = np.linspace(80, 120, 50)
            # Y: Time to Maturity (or whatever is selected as Y, but for surface we usually map 2 inputs to Z)
            # Here we map X and Y inputs to grid axes

            if self.y_axis == "Value":
                 y = np.linspace(0.1, 2, 50) # Time to maturity range
            else:
                 y = np.linspace(0, 1, 50)

            X, Y = np.meshgrid(x, y)

            # Z Calculation (e.g., Implied Vol or Option Value)
            if self.z_axis == "Volatility":
                # Volatility surface smile
                Z = 0.2 + 0.1 * ((X - 100)/100)**2 + 0.05 * np.exp(-Y)
            else:
                # Black-Scholes-like surface shape mock
                Z = np.maximum(X - 100, 0) * np.exp(-0.05 * Y) + 5 * np.exp(-0.5 * ((X-100)/10)**2) * np.sqrt(Y)

            fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Plasma')])
            fig.update_layout(
                title=f"{self.z_axis} Surface ({self.x_axis} vs {self.y_axis})",
                scene=dict(
                    xaxis_title=self.x_axis,
                    yaxis_title=self.y_axis if self.y_axis != "Value" else "Time", # Label tweak for context
                    zaxis_title=self.z_axis
                ),
                template="plotly_white",
                 height=600,
                margin=dict(l=0, r=0, b=0, t=30)
            )
            return fig
