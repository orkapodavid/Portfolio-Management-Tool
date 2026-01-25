import reflex as rx
import plotly.graph_objects as go
import pandas as pd
import numpy as np

class PricerBondState(rx.State):
    x_axis: str = "Maturity"
    y_axis: str = "Yield"
    z_axis: str = "None"

    @rx.var
    def chart(self) -> go.Figure:
        return self.generate_chart()

    def generate_chart(self) -> go.Figure:
        # Generate mock financial data
        np.random.seed(42)
        n_points = 100

        # Create base data
        maturity = np.linspace(1, 30, n_points)
        yield_val = np.log(maturity) * 2 + 1 + np.random.normal(0, 0.2, n_points)
        price = 100 * np.exp(-yield_val/100 * maturity) + np.random.normal(0, 1, n_points)
        coupon = np.random.choice([2.0, 3.0, 4.0, 5.0], n_points)
        duration = maturity * (1 - np.exp(-0.05 * maturity)) / 0.05 # Rough duration approx
        convexity = duration ** 2 / 2

        df = pd.DataFrame({
            "Maturity": maturity,
            "Yield": yield_val,
            "Price": price,
            "Coupon": coupon,
            "Duration": duration,
            "Convexity": convexity
        })

        if self.z_axis == "None":
            # Scenario A (2D): Standard 2D Line/Scatter chart
            # Sort by X axis for cleaner lines if it's a line chart
            df_sorted = df.sort_values(by=self.x_axis)

            fig = go.Figure(data=go.Scatter(
                x=df_sorted[self.x_axis],
                y=df_sorted[self.y_axis],
                mode='lines+markers',
                marker=dict(size=8, color=df_sorted[self.y_axis], colorscale='Viridis', showscale=True)
            ))
            fig.update_layout(
                title=f"{self.y_axis} vs {self.x_axis}",
                xaxis_title=self.x_axis,
                yaxis_title=self.y_axis,
                template="plotly_white",
                height=600,
            )
            return fig
        else:
            # Scenario B (3D): Interactive 3D Scatter Plot
            fig = go.Figure(data=[go.Scatter3d(
                x=df[self.x_axis],
                y=df[self.y_axis],
                z=df[self.z_axis],
                mode='markers',
                marker=dict(
                    size=5,
                    color=df[self.z_axis],
                    colorscale='Viridis',
                    opacity=0.8,
                    showscale=True
                )
            )])
            fig.update_layout(
                title=f"{self.y_axis} vs {self.x_axis} vs {self.z_axis}",
                scene=dict(
                    xaxis_title=self.x_axis,
                    yaxis_title=self.y_axis,
                    zaxis_title=self.z_axis
                ),
                template="plotly_white",
                height=600,
                margin=dict(l=0, r=0, b=0, t=30)
            )
            return fig
