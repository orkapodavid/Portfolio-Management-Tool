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
        np.random.seed(42)

        if self.z_axis == "None":
            # Scenario A (2D): Standard 2D Line/Scatter chart
            n_points = 100
            maturity = np.linspace(1, 30, n_points)
            yield_val = np.log(maturity) * 2 + 1 + np.random.normal(0, 0.2, n_points)
            price = 100 * np.exp(-yield_val/100 * maturity) + np.random.normal(0, 1, n_points)
            coupon = np.random.choice([2.0, 3.0, 4.0, 5.0], n_points)
            duration = maturity * (1 - np.exp(-0.05 * maturity)) / 0.05
            convexity = duration ** 2 / 2
            volatility = np.random.normal(0.2, 0.05, n_points) # Mock volatility

            df = pd.DataFrame({
                "Maturity": maturity,
                "Yield": yield_val,
                "Price": price,
                "Coupon": coupon,
                "Duration": duration,
                "Convexity": convexity,
                "Volatility": volatility
            })

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
            # Scenario B (3D): Surface Plot
            # We need a grid for Surface plots

            # Define ranges for X and Y axes based on selection
            if self.x_axis == "Maturity":
                x = np.linspace(1, 30, 50)
            elif self.x_axis == "Duration":
                x = np.linspace(0, 20, 50)
            else:
                x = np.linspace(0, 100, 50) # Fallback

            if self.y_axis == "Yield":
                y = np.linspace(0, 10, 50)
            elif self.y_axis == "Price":
                y = np.linspace(80, 120, 50)
            else:
                y = np.linspace(0, 100, 50) # Fallback

            X, Y = np.meshgrid(x, y)

            # Calculate Z based on X and Y to create a surface
            if self.z_axis == "Volatility":
                # Volatility surface: often curved
                # Mock: Vol increases with yield (Y) and varies with maturity (X)
                Z = 0.2 + (Y / 20) + np.sin(X / 5) * 0.05
            elif self.z_axis == "Convexity":
                # Convexity usually relates to duration^2
                # Here we mock it based on X (Maturity/Duration) and Y
                Z = (X**2 / 100) + (Y / 10)
            else:
                Z = np.sin(np.sqrt(X**2 + Y**2))

            fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis')])

            fig.update_layout(
                title=f"{self.z_axis} Surface ({self.y_axis} vs {self.x_axis})",
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
