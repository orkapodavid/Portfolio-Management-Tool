"""
Shared AG Grid configuration for consistent UX across all grids.

This module provides a factory function with Tier 1 universal enhancements:
- Status bar with row counts and aggregation
- Range selection for cell blocks
- No-rows overlay for empty states
- Floating filters for quick filtering

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


# =============================================================================
# UNIVERSAL CONFIGURATIONS
# =============================================================================

# Standard status bar for all grids - shows row counts and aggregations
STANDARD_STATUS_BAR = {
    "statusPanels": [
        {"statusPanel": "agTotalRowCountComponent", "align": "left"},
        {"statusPanel": "agFilteredRowCountComponent", "align": "left"},
        {"statusPanel": "agSelectedRowCountComponent", "align": "center"},
        {"statusPanel": "agAggregationComponent", "align": "right"},
    ],
}

# Enhanced default column definition with floating filters
ENHANCED_DEFAULT_COL_DEF = {
    "sortable": True,
    "resizable": True,
    "filter": True,
    "floatingFilter": True,
}

# Standard default column definition (without floating filters)
STANDARD_DEFAULT_COL_DEF = {
    "sortable": True,
    "resizable": True,
    "filter": True,
}

# No-rows overlay message
NO_ROWS_TEMPLATE = (
    '<span style="padding: 10px; color: #6b7280;">No rows to display</span>'
)


# =============================================================================
# FACTORY FUNCTION
# =============================================================================


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

    # Merge any additional kwargs
    grid_props.update(kwargs)

    return ag_grid(**grid_props)


# =============================================================================
# EXPORT HELPER
# =============================================================================


# JavaScript to find AG Grid API reliably
_EXPORT_EXCEL_JS = """(function() {
    // Find the AG Grid root wrapper
    const wrapper = document.querySelector('.ag-root-wrapper');
    if (!wrapper) {
        alert('Grid not found');
        return;
    }
    
    // Find React fiber with grid API
    const key = Object.keys(wrapper).find(k => k.startsWith('__reactFiber'));
    if (!key) {
        alert('Grid API not accessible');
        return;
    }
    
    let fiber = wrapper[key];
    while (fiber) {
        if (fiber.stateNode && fiber.stateNode.api) {
            fiber.stateNode.api.exportDataAsExcel();
            return;
        }
        fiber = fiber.return;
    }
    alert('Grid API not found');
})()"""


def export_button(button_size: str = "2") -> rx.Component:
    """
    Create an Excel export button for AG Grid.

    This button finds the first AG Grid on the page and exports its data.

    Args:
        button_size: Radix button size ("1", "2", "3")

    Returns:
        Excel export button component

    Usage:
        rx.vstack(
            rx.hstack(export_button(), justify="end", width="100%"),
            create_standard_grid(grid_id="my_grid", ...),
        )
    """
    return rx.button(
        rx.icon("file-spreadsheet", size=16),
        "Excel",
        on_click=rx.call_script(_EXPORT_EXCEL_JS),
        variant="soft",
        color_scheme="green",
        size=button_size,
    )


# Legacy alias for backwards compatibility
def export_buttons(
    grid_id: str = "",  # No longer used, kept for compatibility
    *,
    show_excel: bool = True,
    show_csv: bool = False,  # Disabled by default now
    button_size: str = "2",
) -> rx.Component:
    """Legacy wrapper - now just returns export_button()."""
    return rx.hstack(export_button(button_size), spacing="2")


# =============================================================================
# COLUMN STATE PERSISTENCE
# =============================================================================

# JavaScript to get grid API
_GET_GRID_API_JS = """(function() {
    const wrapper = document.querySelector('.ag-root-wrapper');
    if (!wrapper) { return null; }
    const key = Object.keys(wrapper).find(k => k.startsWith('__reactFiber'));
    if (!key) { return null; }
    let fiber = wrapper[key];
    while (fiber) {
        if (fiber.stateNode && fiber.stateNode.api) return fiber.stateNode.api;
        fiber = fiber.return;
    }
    return null;
})()"""


def _get_auto_save_js(storage_key: str) -> str:
    """Generate auto-save JavaScript for column state."""
    return f"""(function() {{
    const api = {_GET_GRID_API_JS};
    if (api) {{
        const state = api.getColumnState();
        localStorage.setItem('{storage_key}', JSON.stringify(state));
    }}
}})()"""


def _get_restore_js(storage_key: str) -> str:
    """Generate restore JavaScript for column state."""
    return f"""(function() {{
    const api = {_GET_GRID_API_JS};
    const state = localStorage.getItem('{storage_key}');
    if (api && state) {{
        api.applyColumnState({{state: JSON.parse(state), applyOrder: true}});
    }}
}})()"""


def _get_reset_js(storage_key: str) -> str:
    """Generate reset JavaScript for column state."""
    return f"""(function() {{
    const api = {_GET_GRID_API_JS};
    if (api) {{
        api.resetColumnState();
        localStorage.removeItem('{storage_key}');
    }}
}})()"""


def column_state_buttons(
    storage_key: str,
    *,
    show_save: bool = False,  # Hidden by default since we auto-save
    show_restore: bool = True,
    show_reset: bool = True,
    button_size: str = "2",
) -> rx.Component:
    """
    Create column state management buttons.

    Args:
        storage_key: Unique localStorage key for this grid's state
        show_save: Show manual Save button (default: False, we auto-save)
        show_restore: Show Restore button
        show_reset: Show Reset button
        button_size: Radix button size

    Returns:
        HStack with column state buttons
    """
    buttons = []

    if show_save:
        buttons.append(
            rx.button(
                rx.icon("save", size=16),
                "Save Layout",
                on_click=rx.call_script(_get_auto_save_js(storage_key)),
                variant="soft",
                color_scheme="green",
                size=button_size,
            )
        )

    if show_restore:
        buttons.append(
            rx.button(
                rx.icon("rotate-ccw", size=16),
                "Restore",
                on_click=rx.call_script(_get_restore_js(storage_key)),
                variant="soft",
                color_scheme="blue",
                size=button_size,
            )
        )

    if show_reset:
        buttons.append(
            rx.button(
                rx.icon("x", size=16),
                "Reset",
                on_click=rx.call_script(_get_reset_js(storage_key)),
                variant="soft",
                color_scheme="gray",
                size=button_size,
            )
        )

    return rx.hstack(*buttons, spacing="2")


def get_column_state_handlers(storage_key: str) -> dict:
    """
    Get event handlers for auto-saving column state.

    Args:
        storage_key: Unique localStorage key for this grid's state

    Returns:
        Dict of event handlers to spread into ag_grid props

    Usage:
        create_standard_grid(
            grid_id="my_grid",
            row_data=State.data,
            column_defs=columns,
            **get_column_state_handlers("my_grid_state"),
        )
    """
    auto_save_script = rx.call_script(_get_auto_save_js(storage_key))
    return {
        "on_column_resized": auto_save_script,
        "on_column_moved": auto_save_script,
        "on_sort_changed": auto_save_script,
        "on_column_visible": auto_save_script,
        "on_column_pinned": auto_save_script,
    }


# =============================================================================
# CONVENIENCE EXPORTS
# =============================================================================

__all__ = [
    "create_standard_grid",
    "export_button",
    "export_buttons",
    "column_state_buttons",
    "get_column_state_handlers",
    "STANDARD_STATUS_BAR",
    "ENHANCED_DEFAULT_COL_DEF",
    "STANDARD_DEFAULT_COL_DEF",
    "NO_ROWS_TEMPLATE",
]
