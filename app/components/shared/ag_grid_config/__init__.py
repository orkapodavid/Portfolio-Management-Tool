"""
Shared AG Grid configuration for consistent UX across all grids.

This package provides factory functions and UI components for standardized
AG Grid usage. All public symbols are re-exported here for backward
compatibility — existing imports continue to work unchanged.

Usage:
    from app.components.shared.ag_grid_config import create_standard_grid

    def my_grid() -> rx.Component:
        return create_standard_grid(
            grid_id="my_grid",
            row_data=State.data,
            column_defs=get_columns(),
            enable_cell_flash=True,  # For real-time grids
        )
"""

# --- Constants ---
from .constants import (
    COMPACT_HEADER_HEIGHT,
    COMPACT_ROW_HEIGHT,
    ENHANCED_DEFAULT_COL_DEF,
    NO_ROWS_TEMPLATE,
    STANDARD_DEFAULT_COL_DEF,
    STANDARD_STATUS_BAR,
)

# --- Grid factory ---
from .grid_factory import create_standard_grid

# --- Export helpers ---
from .export_helpers import get_default_csv_export_params, get_default_export_params

# --- State persistence ---
from .state_persistence import grid_state_script

# --- Toolbar ---
from .toolbar import grid_toolbar

# --- Filter bar ---
from .filter_bar import (
    FILTER_BTN_CLASS,
    FILTER_INPUT_CLASS,
    FILTER_LABEL_CLASS,
    filter_date_input,
    filter_date_range_bar,
)

# --- Context menu ---
from .context_menu import build_context_menu, context_menu_dispatch_input

__all__ = [
    # Grid factory
    "create_standard_grid",
    # State persistence
    "grid_state_script",
    # Toolbar
    "grid_toolbar",
    # Export helpers
    "get_default_export_params",
    "get_default_csv_export_params",
    # Filter bar
    "filter_date_input",
    "filter_date_range_bar",
    "FILTER_LABEL_CLASS",
    "FILTER_INPUT_CLASS",
    "FILTER_BTN_CLASS",
    # Context menu
    "build_context_menu",
    "context_menu_dispatch_input",
    # Constants
    "STANDARD_STATUS_BAR",
    "ENHANCED_DEFAULT_COL_DEF",
    "STANDARD_DEFAULT_COL_DEF",
    "NO_ROWS_TEMPLATE",
    "COMPACT_ROW_HEIGHT",
    "COMPACT_HEADER_HEIGHT",
]
