"""
AG Grid Constants

Grid IDs, route mappings, and row identification configuration
for notification navigation.
"""

from enum import StrEnum


# =============================================================================
# AG GRID ID REGISTRY
# =============================================================================


class GridId(StrEnum):
    """Enum of all AG Grid IDs in the application.

    Use these constants for notification navigation and grid targeting.
    """

    # Dashboard
    MARKET_DATA = "market_data_grid"

    # Market Data
    FX_DATA = "fx_data_grid"
    REFERENCE_DATA = "reference_data_grid"


# Grid to route mapping for notification navigation
GRID_ROUTES: dict[str, str] = {
    GridId.MARKET_DATA: "/dashboard/analytics",
    GridId.FX_DATA: "/market-data/fx-data",
    GridId.REFERENCE_DATA: "/market-data/reference-data",
}


# Grid row ID configuration for notification navigation
# Each entry specifies the field used to identify rows in that grid
GRID_ROW_ID_CONFIG: dict[str, str] = {
    GridId.MARKET_DATA: "ticker",
    GridId.FX_DATA: "pair",
    GridId.REFERENCE_DATA: "ticker",
}


def get_grid_row_id_key(grid_id: str) -> str:
    """Get the row ID key for a grid.

    Args:
        grid_id: The grid ID string

    Returns:
        The field name used for row identification. Defaults to "id".
    """
    return GRID_ROW_ID_CONFIG.get(grid_id, "id")
