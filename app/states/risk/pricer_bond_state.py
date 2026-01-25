import reflex as rx
import plotly.graph_objects as go
import numpy as np

class PricerBondState(rx.State):
    x_axis: str = "Maturity"
    y_axis: str = "Yield"
    z_axis: str = "None"

    @rx.var
    def chart(self) -> go.Figure:
        return self.generate_chart()

    def generate_chart(self) -> go.Figure:
        # Mock data generation
        if self.z_axis == "None":
            # 2D Chart: Yield Curve (Maturity vs Yield) as an example
            x_vals = np.linspace(1, 30, 100)

            # Simple mock function for yield curve
            if self.y_axis == "Yield":
                y_vals = np.log(x_vals) * 2 + 1 + np.random.normal(0, 0.1, 100)
            else:
                y_vals = np.sin(x_vals) * 10 + 90  # Random price-like movement

            fig = go.Figure(data=go.Scatter(x=x_vals, y=y_vals, mode='lines+markers'))
            fig.update_layout(
                title=f"{self.y_axis} vs {self.x_axis}",
                xaxis_title=self.x_axis,
                yaxis_title=self.y_axis,
                template="plotly_white"
            )
            return fig
        else:
            # 3D Chart
            x = np.linspace(1, 30, 30)
            y = np.linspace(0, 10, 30)
            X, Y = np.meshgrid(x, y)

            # Mock surface
            Z = np.sin(X/5) * np.cos(Y/2) * 10 + 100

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
