"""
Core Bond Pricer for Portfolio Management Tool.

Provides bond pricing calculations and data generation:
- Yield curve data
- Price calculations
- Surface data for 3D analysis (coupon, convexity)

TODO: Replace mock formulas with real pricing engine.
"""

import logging
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)


class BondPricer:
    """
    Core bond pricing calculations.

    Generates yield curves, price data, and 3D surface grids
    for bond analysis. Currently uses mock formulas.
    """

    def __init__(
        self,
        coupon_rate: float = 4.5,
        maturity_range: tuple[float, float] = (1, 30),
        yield_range: tuple[float, float] = (2, 8),
        num_points: int = 30,
    ):
        """
        Initialize bond pricer.

        Args:
            coupon_rate: Annual coupon rate (%)
            maturity_range: (min, max) maturity in years
            yield_range: (min, max) yield in %
            num_points: Number of data points per axis
        """
        self.coupon_rate = coupon_rate
        self.maturity_range = maturity_range
        self.yield_range = yield_range
        self.num_points = num_points

    def generate_maturities(self) -> np.ndarray:
        """Generate maturity axis values."""
        return np.linspace(
            self.maturity_range[0], self.maturity_range[1], self.num_points
        )

    def generate_yields(self) -> np.ndarray:
        """Generate yield axis values."""
        return np.linspace(
            self.yield_range[0], self.yield_range[1], self.num_points
        )

    def calculate_yield_curve(self, maturities: np.ndarray) -> np.ndarray:
        """
        Calculate yield curve values for given maturities.

        Args:
            maturities: Array of maturity values

        Returns:
            Array of yield values (logarithmic mock curve)
        """
        return np.log(maturities) + 2

    def calculate_prices(self, maturities: np.ndarray) -> np.ndarray:
        """
        Calculate bond prices for given maturities.

        Args:
            maturities: Array of maturity values

        Returns:
            Array of price values
        """
        return 100 - maturities

    def calculate_duration(self, maturities: np.ndarray) -> np.ndarray:
        """
        Calculate duration for given maturities.

        Args:
            maturities: Array of maturity values

        Returns:
            Array of duration values (mock: 0.8 * maturity)
        """
        return maturities * 0.8

    def generate_curve_data(
        self, x_axis: str, y_axis: str
    ) -> dict[str, np.ndarray]:
        """
        Generate 2D curve data for the given axis selections.

        Args:
            x_axis: X-axis metric name (Maturity, Duration)
            y_axis: Y-axis metric name (Yield, Price)

        Returns:
            Dictionary with x_values, y_values, x_label, y_label
        """
        maturities = self.generate_maturities()

        # Build data arrays
        data = {
            "Maturity": maturities,
            "Yield": self.calculate_yield_curve(maturities),
            "Price": self.calculate_prices(maturities),
        }

        # Add Duration if requested
        if x_axis == "Duration":
            data["Duration"] = self.calculate_duration(maturities)

        return {
            "x_values": data.get(x_axis, maturities),
            "y_values": data.get(y_axis, data["Yield"]),
            "x_label": x_axis,
            "y_label": y_axis,
        }

    def generate_surface_data(
        self, z_axis: str
    ) -> dict[str, np.ndarray | str]:
        """
        Generate 3D surface data for the given Z-axis selection.

        Args:
            z_axis: Z-axis metric name (Coupon, Convexity)

        Returns:
            Dictionary with X_grid, Y_grid, Z_grid, colorscale
        """
        maturities = self.generate_maturities()
        yields = self.generate_yields()
        X_grid, Y_grid = np.meshgrid(maturities, yields)

        if z_axis == "Coupon":
            # Price/Coupon sensitivity
            Z_grid = (X_grid * Y_grid) / 5 + np.sin(X_grid / 5) * 5
            colorscale = "Viridis"
        elif z_axis == "Convexity":
            # Convexity shape (smile/bowl)
            Z_grid = (Y_grid - 5) ** 2 + (X_grid / 10)
            colorscale = "Plasma"
        else:
            Z_grid = X_grid * Y_grid
            colorscale = "Blues"

        return {
            "X_grid": X_grid,
            "Y_grid": Y_grid,
            "Z_grid": Z_grid,
            "colorscale": colorscale,
        }
