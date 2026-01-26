import reflex as rx
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


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

    def update_chart(self):
        """Regenerate the chart based on axes selection."""

        # 1. GENERATE MOCK DATA
        # We need a range of values to create a surface
        maturities = np.linspace(1, 30, 30)  # 1 to 30 years
        yields = np.linspace(2, 8, 30)  # 2% to 8% yield

        # 2. LOGIC SWITCH: 2D vs 3D
        if self.z_axis == "None":
            # --- 2D SCENARIO (Simple Line/Scatter) ---
            # Just create a simple curve for the current view
            df = pd.DataFrame(
                {
                    "Maturity": maturities,
                    "Yield": np.log(maturities) + 2,  # Mock curve
                    "Price": 100 - maturities,
                }
            )

            # Map selection to dataframe columns
            x_col = self.x_axis
            y_col = self.y_axis

            # Create 2D Line Chart
            # Handle Duration mapping if selected
            if x_col == "Duration":
                # Mock duration
                df["Duration"] = df["Maturity"] * 0.8

            fig = px.line(
                df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}", markers=True
            )
            fig.update_layout(
                template="plotly_white", height=500, margin=dict(l=20, r=20, t=50, b=20)
            )
            self.figure = fig

        else:
            # --- 3D SCENARIO (Surface Plot) ---
            # CRITICAL: Create a Meshgrid (Matrix) for Surface Plots
            # X_grid and Y_grid become 2D arrays covering every combination
            X_grid, Y_grid = np.meshgrid(maturities, yields)

            # Calculate Z based on the Z-Axis selection using mathematical relationships
            # This ensures we get a nice smooth surface shape
            if self.z_axis == "Coupon":
                # Mock formula: Price/Coupon sensitivity
                # Z = (X * Y) / 10 + curve
                Z_grid = (X_grid * Y_grid) / 5 + np.sin(X_grid / 5) * 5
                colorscale = "Viridis"
            elif self.z_axis == "Convexity":
                # Mock formula: Convexity shape (usually a smile or bowl)
                Z_grid = (Y_grid - 5) ** 2 + (X_grid / 10)
                colorscale = "Plasma"
            else:
                Z_grid = X_grid * Y_grid
                colorscale = "Blues"

            # Create 3D Surface Plot
            fig = go.Figure(
                data=[
                    go.Surface(
                        x=X_grid,
                        y=Y_grid,
                        z=Z_grid,
                        colorscale=colorscale,
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
                    aspectratio=dict(
                        x=1, y=1, z=0.7
                    ),  # Flattens z-axis slightly for better view
                    camera=dict(
                        eye=dict(x=1.5, y=1.5, z=1.2)  # Set default camera angle
                    ),
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
