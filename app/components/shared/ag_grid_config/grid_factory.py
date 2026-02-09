"""
AG Grid factory function — creates a standard grid with Tier 1/2 enhancements.

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

import reflex as rx
from reflex_ag_grid import ag_grid

from .constants import (
    COMPACT_HEADER_HEIGHT,
    COMPACT_ROW_HEIGHT,
    ENHANCED_DEFAULT_COL_DEF,
    NO_ROWS_TEMPLATE,
    STANDARD_DEFAULT_COL_DEF,
    STANDARD_STATUS_BAR,
)


def create_standard_grid(
    grid_id: str,
    row_data,
    column_defs: list,
    row_id_key: str = "id",
    *,
    # Tier 1 enhancements (enabled by default)
    enable_status_bar: bool = True,
    enable_range_selection: bool = True,
    enable_floating_filters: bool = True,
    enable_no_rows_overlay: bool = True,
    # Tier 2 enhancements (opt-in)
    enable_cell_flash: bool = False,
    enable_row_numbers: bool = False,
    enable_multi_select: bool = False,
    enable_compact_mode: bool = False,
    # Notification navigation (enabled by default for consistency)
    enable_notification_jump: bool = True,
    # Loading overlay (for force refresh pattern)
    loading: rx.Var[bool] | bool = False,
    loading_template: str = "<span class='ag-overlay-loading-center'>Loading...</span>",
    # Layout
    height: str = "100%",
    width: str = "100%",
    # Override defaults
    default_col_def: dict | None = None,
    status_bar: dict | None = None,
    # Pass-through kwargs
    **kwargs,
) -> rx.Component:
    """
    Factory for standard AG Grid with Tier 1 enhancements.

    Args:
        grid_id: Unique identifier for the grid
        row_data: State variable containing row data
        column_defs: List of column definitions
        row_id_key: Field name for unique row ID

        enable_status_bar: Show status bar with row counts (default: True)
        enable_range_selection: Allow drag-selection of cell ranges (default: True)
        enable_floating_filters: Show quick-filter row under headers (default: True)
        enable_no_rows_overlay: Show message when data is empty (default: True)

        enable_cell_flash: Flash cells on value change, for real-time grids (default: False)
        enable_row_numbers: Show auto-numbered row column (default: False)
        enable_multi_select: Enable multi-row selection with checkboxes (default: False)
        enable_notification_jump: Enable jump-to-row from notification sidebar (default: False)

        height: Grid height CSS value (default: "100%")
        width: Grid width CSS value (default: "100%")

        default_col_def: Override default column definition
        status_bar: Override status bar configuration
        **kwargs: Additional AG Grid props

    Returns:
        AG Grid component with standard enhancements
    """
    # Build default col def
    if default_col_def is None:
        default_col_def = (
            ENHANCED_DEFAULT_COL_DEF
            if enable_floating_filters
            else STANDARD_DEFAULT_COL_DEF
        )

    # Build grid props
    grid_props = {
        "id": grid_id,
        "row_data": row_data,
        "column_defs": column_defs,
        "row_id_key": row_id_key,
        "theme": "quartz",
        "default_col_def": default_col_def,
        "height": height,
        "width": width,
    }

    # Tier 1: Status bar
    if enable_status_bar:
        grid_props["status_bar"] = status_bar or STANDARD_STATUS_BAR

    # Tier 1: Range selection
    if enable_range_selection:
        grid_props["enable_range_selection"] = True
        grid_props["cell_selection"] = True

    # Tier 1: No-rows overlay
    if enable_no_rows_overlay:
        grid_props["overlay_no_rows_template"] = NO_ROWS_TEMPLATE

    # Tier 2: Cell flash (for real-time grids)
    if enable_cell_flash:
        grid_props["enable_cell_change_flash"] = True

    # Tier 2: Row numbers
    if enable_row_numbers:
        grid_props["row_numbers"] = True

    # Tier 2: Multi-row selection with checkboxes
    if enable_multi_select:
        grid_props["row_selection"] = "multiple"

    # Tier 2: Compact mode (dense rows)
    if enable_compact_mode:
        grid_props["row_height"] = COMPACT_ROW_HEIGHT
        grid_props["header_height"] = COMPACT_HEADER_HEIGHT

    # Notification jump (wire on_grid_ready to check for pending highlights)
    if enable_notification_jump:
        from app.states.notifications import NotificationSidebarState
        grid_props["on_grid_ready"] = NotificationSidebarState.execute_pending_highlight(grid_id)

    # Loading overlay (for force refresh pattern)
    grid_props["loading"] = loading
    grid_props["overlay_loading_template"] = loading_template

    # Merge any additional kwargs
    grid_props.update(kwargs)

    return ag_grid(**grid_props)
