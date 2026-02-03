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

from typing import Callable

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

# Compact mode configuration - reduces row height for dense data display
COMPACT_ROW_HEIGHT = 28  # Default is ~42px, compact is 28px
COMPACT_HEADER_HEIGHT = 32  # Slightly reduced header


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
    enable_multi_select: bool = False,
    enable_compact_mode: bool = False,
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

    # Merge any additional kwargs
    grid_props.update(kwargs)

    return ag_grid(**grid_props)


# =============================================================================
# DEFAULT EXPORT PARAMS
# =============================================================================


def _get_filename_js(page_name: str) -> str:
    """Generate JS function that creates timestamped filename."""
    return f"""(() => {{
        const now = new Date();
        const yyyy = now.getFullYear();
        const mm = String(now.getMonth() + 1).padStart(2, '0');
        const dd = String(now.getDate()).padStart(2, '0');
        const hh = String(now.getHours()).padStart(2, '0');
        const min = String(now.getMinutes()).padStart(2, '0');
        return '{page_name}_' + yyyy + mm + dd + '_' + hh + min;
    }})()"""


# JavaScript callback: Skip unselected rows ONLY if some rows are selected
# If no rows are selected, export all rows (don't skip any)
_SHOULD_ROW_BE_SKIPPED_JS = rx.Var("""(params) => {
    const selectedRows = params.api.getSelectedRows();
    if (selectedRows.length === 0) {
        // No selection: export all rows
        return false;
    }
    // Has selection: skip if not selected
    return !params.node.isSelected();
}""")


def get_default_export_params(page_name: str) -> rx.Var:
    """
    Generate default Excel export params with timestamped filename.

    This is used for the context menu "Export to Excel" option.
    Features:
    - Dynamic timestamped filename: <page_name>_YYYYMMDD_HHMM.xlsx
    - Exports only selected rows if any are selected
    - Exports all rows if no selection

    Args:
        page_name: Name prefix for the export file (e.g., "pnl_full")

    Returns:
        rx.Var containing export params with dynamic fileName and row filtering

    Usage:
        create_standard_grid(
            grid_id="my_grid",
            ...,
            default_excel_export_params=get_default_export_params("pnl_full"),
        )
    """
    return rx.Var.create(
        {
            "fileName": rx.Var(_get_filename_js(page_name)),
            "shouldRowBeSkipped": _SHOULD_ROW_BE_SKIPPED_JS,
        }
    )


def get_default_csv_export_params(page_name: str) -> rx.Var:
    """
    Generate default CSV export params with timestamped filename.

    This is used for the context menu "Export to CSV" option.
    Features:
    - Dynamic timestamped filename: <page_name>_YYYYMMDD_HHMM.csv
    - Exports only selected rows if any are selected
    - Exports all rows if no selection

    Args:
        page_name: Name prefix for the export file (e.g., "pnl_full")

    Returns:
        rx.Var containing export params with dynamic fileName and row filtering

    Usage:
        create_standard_grid(
            grid_id="my_grid",
            ...,
            default_csv_export_params=get_default_csv_export_params("pnl_full"),
        )
    """
    return rx.Var.create(
        {
            "fileName": rx.Var(_get_filename_js(page_name)),
            "shouldRowBeSkipped": _SHOULD_ROW_BE_SKIPPED_JS,
        }
    )


# =============================================================================
# EXPORT HELPER
# =============================================================================


# JavaScript to find AG Grid API reliably
_GET_GRID_API_JS = """(function() {
    const wrapper = document.querySelector('.ag-root-wrapper');
    if (!wrapper) return null;
    const key = Object.keys(wrapper).find(k => k.startsWith('__reactFiber'));
    if (!key) return null;
    let fiber = wrapper[key];
    while (fiber) {
        if (fiber.stateNode && fiber.stateNode.api) return fiber.stateNode.api;
        fiber = fiber.return;
    }
    return null;
})()"""


def _get_export_excel_js(page_name: str) -> str:
    """
    Generate JavaScript for Excel export with timestamped filename.

    Args:
        page_name: Name to prefix the filename (e.g., "pnl_full")

    Returns:
        JS code that exports with filename: <page_name>_YYYYMMDD_HHMM.xlsx
    """
    return f"""(function() {{
    // Find the AG Grid root wrapper
    const wrapper = document.querySelector('.ag-root-wrapper');
    if (!wrapper) {{
        alert('Grid not found');
        return;
    }}
    
    // Find React fiber with grid API
    const key = Object.keys(wrapper).find(k => k.startsWith('__reactFiber'));
    if (!key) {{
        alert('Grid API not accessible');
        return;
    }}
    
    let fiber = wrapper[key];
    while (fiber) {{
        if (fiber.stateNode && fiber.stateNode.api) {{
            const api = fiber.stateNode.api;
            
            // Generate timestamp: YYYYMMDD_HHMM
            const now = new Date();
            const yyyy = now.getFullYear();
            const mm = String(now.getMonth() + 1).padStart(2, '0');
            const dd = String(now.getDate()).padStart(2, '0');
            const hh = String(now.getHours()).padStart(2, '0');
            const min = String(now.getMinutes()).padStart(2, '0');
            const timestamp = `${{yyyy}}${{mm}}${{dd}}_${{hh}}${{min}}`;
            
            // Check if any rows are selected
            const selectedRows = api.getSelectedRows();
            const hasSelection = selectedRows.length > 0;
            
            // Export with conditional row filtering
            api.exportDataAsExcel({{
                fileName: '{page_name}_' + timestamp,
                shouldRowBeSkipped: (params) => {{
                    if (!hasSelection) return false;  // No selection: export all
                    return !params.node.isSelected();  // Skip non-selected rows
                }}
            }});
            return;
        }}
        fiber = fiber.return;
    }}
    alert('Grid API not found');
}})()"""


def export_button(page_name: str = "export", button_size: str = "2") -> rx.Component:
    """
    Create an Excel export button for AG Grid with timestamped filename.

    This button finds the first AG Grid on the page and exports its data
    with a filename in the format: <page_name>_YYYYMMDD_HHMM.xlsx

    Args:
        page_name: Name prefix for the export file (e.g., "pnl_full", "undertakings")
        button_size: Radix button size ("1", "2", "3")

    Returns:
        Excel export button component

    Usage:
        rx.vstack(
            rx.hstack(export_button(page_name="pnl_full"), justify="end", width="100%"),
            create_standard_grid(grid_id="my_grid", ...),
        )
    """
    return rx.button(
        rx.icon("file-spreadsheet", size=16),
        "Excel",
        on_click=rx.call_script(_get_export_excel_js(page_name)),
        variant="soft",
        color_scheme="green",
        size=button_size,
    )


# Legacy alias for backwards compatibility
def export_buttons(
    grid_id: str = "",  # No longer used, kept for compatibility
    *,
    page_name: str = "export",
    show_excel: bool = True,
    show_csv: bool = False,  # Disabled by default now
    button_size: str = "2",
) -> rx.Component:
    """Legacy wrapper - now just returns export_button()."""
    return rx.hstack(export_button(page_name, button_size), spacing="2")


# =============================================================================
# GRID STATE PERSISTENCE (Full: columns + filters + sort)
# =============================================================================

# The new approach uses getState()/setState() API for complete grid state.
# This captures column widths/order, filters, and sorting in one call.


def grid_state_script(storage_key: str) -> str:
    """
    Generate client-side JavaScript for full grid state persistence.

    This script provides:
    - getGridApi_{key}(): Helper to access AG Grid API from React Fiber
    - saveGridState_{key}(): Save complete grid state to localStorage
    - restoreGridState_{key}(): Restore state with flex removal fix
    - resetGridState_{key}(): Reset grid to defaults
    - Auto-restore on page load using polling (works in SPA)

    Args:
        storage_key: Unique localStorage key for this grid's state

    Returns:
        JavaScript code string to be used with rx.script()

    Usage:
        rx.script(grid_state_script("my_grid_state"))
    """
    # Sanitize key for use as JS function suffix (replace dashes with underscores)
    safe_key = storage_key.replace("-", "_")

    return f"""
// Grid State Management for {storage_key}
// Uses AG Grid's getState()/setState() API for complete state persistence

function getGridApi_{safe_key}() {{
    const wrapper = document.querySelector('.ag-root-wrapper');
    if (!wrapper) return null;

    const key = Object.keys(wrapper).find(k => k.startsWith('__reactFiber'));
    if (!key) return null;

    let fiber = wrapper[key];
    let maxDepth = 50;
    while (fiber && maxDepth-- > 0) {{
        if (fiber.stateNode && typeof fiber.stateNode.api === 'object' && fiber.stateNode.api !== null) {{
            if (typeof fiber.stateNode.api.getState === 'function') {{
                return fiber.stateNode.api;
            }}
        }}
        if (fiber.memoizedProps && fiber.memoizedProps.gridRef && fiber.memoizedProps.gridRef.current) {{
            const api = fiber.memoizedProps.gridRef.current.api;
            if (api && typeof api.getState === 'function') {{
                return api;
            }}
        }}
        fiber = fiber.return;
    }}
    return null;
}}

function saveGridState_{safe_key}() {{
    const api = getGridApi_{safe_key}();
    if (api) {{
        const state = api.getState();
        localStorage.setItem('{storage_key}', JSON.stringify(state));
        const parts = [];
        if (state.column) parts.push('columns');
        if (state.filter) parts.push('filters');
        if (state.sort) parts.push('sort');
        console.log('Saved grid state:', parts.join(', '));
    }} else {{
        console.warn('Grid API not ready for save');
    }}
}}

function restoreGridState_{safe_key}() {{
    const api = getGridApi_{safe_key}();
    const stateStr = localStorage.getItem('{storage_key}');
    if (api && stateStr) {{
        try {{
            const state = JSON.parse(stateStr);
            // Fix flex issue: remove flex from column state so widths apply
            if (state.column && state.column.columns) {{
                state.column.columns = state.column.columns.map(col => {{
                    const newCol = {{...col}};
                    delete newCol.flex;
                    return newCol;
                }});
            }}
            api.setState(state);
            console.log('Restored grid state');
        }} catch (e) {{
            console.error('Restore failed:', e);
        }}
    }} else if (!stateStr) {{
        console.log('No saved state found');
    }}
}}

function resetGridState_{safe_key}() {{
    const api = getGridApi_{safe_key}();
    if (api) {{
        api.resetColumnState();
        api.setFilterModel(null);
        localStorage.removeItem('{storage_key}');
        console.log('Reset grid state');
    }}
}}

// Auto-restore on page load (polling for SPA)
(function() {{
    let attempts = 0;
    const maxAttempts = 30;

    const tryRestore = setInterval(() => {{
        attempts++;
        const api = getGridApi_{safe_key}();
        const stateStr = localStorage.getItem('{storage_key}');

        if (api && stateStr) {{
            clearInterval(tryRestore);
            setTimeout(() => {{
                try {{
                    const state = JSON.parse(stateStr);
                    // Fix flex issue
                    if (state.column && state.column.columns) {{
                        state.column.columns = state.column.columns.map(col => {{
                            const newCol = {{...col}};
                            delete newCol.flex;
                            return newCol;
                        }});
                    }}
                    api.setState(state);
                    console.log('Auto-restored grid state after', attempts, 'attempts');
                }} catch (e) {{
                    console.error('Auto-restore failed:', e);
                }}
            }}, 100);
        }} else if (attempts >= maxAttempts) {{
            clearInterval(tryRestore);
        }}
    }}, 500);
}})();
"""


def grid_state_buttons(
    storage_key: str,
    *,
    show_save: bool = True,
    show_restore: bool = True,
    show_reset: bool = True,
    button_size: str = "2",
) -> rx.Component:
    """
    Create grid state management buttons.

    These buttons call the JavaScript functions generated by grid_state_script().
    Make sure to include rx.script(grid_state_script(storage_key)) in your component.

    Args:
        storage_key: Unique localStorage key (must match grid_state_script)
        show_save: Show Save button
        show_restore: Show Restore button
        show_reset: Show Reset button
        button_size: Radix button size

    Returns:
        HStack with grid state buttons
    """
    safe_key = storage_key.replace("-", "_")
    buttons = []

    if show_save:
        buttons.append(
            rx.button(
                rx.icon("save", size=16),
                "Save Layout",
                on_click=rx.call_script(f"saveGridState_{safe_key}()"),
                variant="soft",
                color_scheme="blue",  # Blue to match Restore (both are layout actions)
                size=button_size,
            )
        )

    if show_restore:
        buttons.append(
            rx.button(
                rx.icon("rotate-ccw", size=16),
                "Restore",
                on_click=rx.call_script(f"restoreGridState_{safe_key}()"),
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
                on_click=rx.call_script(f"resetGridState_{safe_key}()"),
                variant="soft",
                color_scheme="gray",
                size=button_size,
            )
        )

    return rx.hstack(*buttons, spacing="2")


def grid_toolbar(
    storage_key: str,
    page_name: str,
    *,
    search_value: rx.Var[str] | None = None,
    on_search_change: Callable | None = None,
    on_search_clear: Callable | None = None,
    show_excel: bool = True,
    show_save: bool = True,
    show_restore: bool = True,
    show_reset: bool = True,
    button_size: str = "2",
    grid_id: str | None = None,
    show_compact_toggle: bool = False,
) -> rx.Component:
    """
    Create a complete grid toolbar with search, export, and layout controls.

    This is the recommended way to add a toolbar above AG Grid components.
    It groups buttons by function with visual dividers for better UX.

    Color scheme:
    - Compact Toggle: Violet (view action)
    - Excel: Green (data export action)
    - Save Layout: Blue (layout action, matches Restore)
    - Restore: Blue (layout action)
    - Reset: Gray (destructive/neutral)

    Args:
        storage_key: Unique localStorage key for grid state persistence
        page_name: Name prefix for export files (e.g., "pnl_full")
        search_value: State var for search text (optional)
        on_search_change: Handler for search input changes (optional)
        on_search_clear: Handler for clearing search (optional)
        show_excel: Show Excel export button
        show_save: Show Save Layout button
        show_restore: Show Restore button
        show_reset: Show Reset button
        button_size: Radix button size
        grid_id: Grid ID for API calls (required for compact toggle)
        show_compact_toggle: Show compact mode toggle button

    Returns:
        Complete toolbar with search (left) and buttons (right)

    Usage:
        grid_toolbar(
            storage_key="pnl_grid_state",
            page_name="pnl_full",
            search_value=State.search_text,
            on_search_change=State.set_search,
            on_search_clear=State.clear_search,
        )
    """
    safe_key = storage_key.replace("-", "_")

    # Build left side (search)
    left_side = []
    if search_value is not None and on_search_change is not None:
        left_side.append(
            quick_filter_input(
                search_value=search_value,
                on_change=on_search_change,
                on_clear=on_search_clear,
            )
        )

    # Build right side (buttons with divider)
    export_buttons = []
    layout_buttons = []

    # Export group (green)
    if show_excel:
        export_buttons.append(
            rx.button(
                rx.icon("file-spreadsheet", size=16),
                "Excel",
                on_click=rx.call_script(_get_export_excel_js(page_name)),
                variant="soft",
                color_scheme="green",
                size=button_size,
            )
        )

    # Layout group (blue/gray)
    if show_save:
        layout_buttons.append(
            rx.button(
                rx.icon("save", size=16),
                "Save Layout",
                on_click=rx.call_script(f"saveGridState_{safe_key}()"),
                variant="soft",
                color_scheme="blue",
                size=button_size,
            )
        )

    if show_restore:
        layout_buttons.append(
            rx.button(
                rx.icon("rotate-ccw", size=16),
                "Restore",
                on_click=rx.call_script(f"restoreGridState_{safe_key}()"),
                variant="soft",
                color_scheme="blue",
                size=button_size,
            )
        )

    if show_reset:
        layout_buttons.append(
            rx.button(
                rx.icon("x", size=16),
                "Reset",
                on_click=rx.call_script(f"resetGridState_{safe_key}()"),
                variant="soft",
                color_scheme="gray",
                size=button_size,
            )
        )

    # View group (violet) - compact mode toggle
    view_buttons = []
    if show_compact_toggle and grid_id:
        # JavaScript to toggle compact mode dynamically via AG Grid API
        # Uses React Fiber traversal to reliably access the grid API
        toggle_compact_js = f"""(function() {{
    // Find the AG Grid root wrapper
    const wrapper = document.querySelector('.ag-root-wrapper');
    if (!wrapper) {{
        console.error('Grid not found');
        return;
    }}
    
    // Find React fiber with grid API
    const key = Object.keys(wrapper).find(k => k.startsWith('__reactFiber'));
    if (!key) {{
        console.error('Grid API not accessible');
        return;
    }}
    
    let fiber = wrapper[key];
    while (fiber) {{
        if (fiber.stateNode && fiber.stateNode.api) {{
            const api = fiber.stateNode.api;
            
            // Get current row height to determine mode
            const firstRow = api.getDisplayedRowAtIndex(0);
            const currentHeight = firstRow ? firstRow.rowHeight : 42;
            const isCompact = currentHeight < 35;
            
            // Toggle between normal and compact
            const newRowHeight = isCompact ? 42 : {COMPACT_ROW_HEIGHT};
            const newHeaderHeight = isCompact ? 48 : {COMPACT_HEADER_HEIGHT};
            
            api.setGridOption('rowHeight', newRowHeight);
            api.setGridOption('headerHeight', newHeaderHeight);
            api.resetRowHeights();
            
            // Auto-size columns for tighter fit in compact mode
            if (!isCompact) {{
                // Switching TO compact: auto-size columns to content
                api.autoSizeAllColumns();
            }} else {{
                // Switching to normal: size columns to fit grid width
                api.sizeColumnsToFit();
            }}
            
            // Update button visual state
            const btn = document.getElementById('compact-toggle-{grid_id}');
            if (btn) {{
                const textNode = btn.querySelector('span:last-child') || btn.lastChild;
                if (!isCompact) {{
                    // Now compact - show active state
                    btn.setAttribute('data-accent-color', 'green');
                    btn.style.setProperty('--accent-9', 'var(--green-9)');
                    btn.style.setProperty('--accent-a3', 'var(--green-a3)');
                    if (textNode) textNode.textContent = 'Compact ✓';
                }} else {{
                    // Now normal - show default state
                    btn.setAttribute('data-accent-color', 'violet');
                    btn.style.removeProperty('--accent-9');
                    btn.style.removeProperty('--accent-a3');
                    if (textNode) textNode.textContent = 'Compact';
                }}
            }}
            
            console.log('Compact mode:', !isCompact, 'Row height:', newRowHeight);
            return;
        }}
        fiber = fiber.return;
    }}
    console.error('Grid API not found in fiber tree');
}})();"""
        view_buttons.append(
            rx.button(
                rx.icon("rows-3", size=16),
                "Compact",
                id=f"compact-toggle-{grid_id}",
                on_click=rx.call_script(toggle_compact_js),
                variant="soft",
                color_scheme="violet",
                size=button_size,
            )
        )

    # Combine with visual divider between groups
    right_items = []

    # View group (leftmost)
    if view_buttons:
        right_items.append(rx.hstack(*view_buttons, spacing="2"))

    if view_buttons and (export_buttons or layout_buttons):
        # Vertical divider
        right_items.append(
            rx.box(
                width="1px",
                height="24px",
                background_color="var(--gray-6)",
            )
        )

    if export_buttons:
        right_items.append(rx.hstack(*export_buttons, spacing="2"))

    if export_buttons and layout_buttons:
        # Vertical divider
        right_items.append(
            rx.box(
                width="1px",
                height="24px",
                background_color="var(--gray-6)",
            )
        )

    if layout_buttons:
        right_items.append(rx.hstack(*layout_buttons, spacing="2"))

    right_side = rx.hstack(*right_items, spacing="3", align="center")

    return rx.hstack(
        *left_side,
        right_side,
        justify="between",
        width="100%",
        padding_bottom="2",
    )


# =============================================================================
# LEGACY: Column State Persistence (Deprecated - use grid_state_* instead)
# =============================================================================


def _get_auto_save_js(storage_key: str) -> str:
    """DEPRECATED: Use grid_state_script() instead."""
    return f"""(function() {{
    const api = {_GET_GRID_API_JS};
    if (api) {{
        const state = api.getColumnState();
        localStorage.setItem('{storage_key}', JSON.stringify(state));
    }}
}})()"""


def _get_restore_js(storage_key: str) -> str:
    """DEPRECATED: Use grid_state_script() instead."""
    return f"""(function() {{
    const api = {_GET_GRID_API_JS};
    const state = localStorage.getItem('{storage_key}');
    if (api && state) {{
        api.applyColumnState({{state: JSON.parse(state), applyOrder: true}});
    }}
}})()"""


def _get_reset_js(storage_key: str) -> str:
    """DEPRECATED: Use grid_state_script() instead."""
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
    show_save: bool = False,
    show_restore: bool = True,
    show_reset: bool = True,
    button_size: str = "2",
) -> rx.Component:
    """DEPRECATED: Use grid_state_buttons() with grid_state_script() instead."""
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
    """DEPRECATED: Not needed with new grid_state_* approach."""
    auto_save_script = rx.call_script(_get_auto_save_js(storage_key))
    return {
        "on_column_resized": auto_save_script,
        "on_column_moved": auto_save_script,
        "on_sort_changed": auto_save_script,
        "on_column_visible": auto_save_script,
        "on_column_pinned": auto_save_script,
    }


# =============================================================================
# QUICK FILTER INPUT
# =============================================================================


def quick_filter_input(
    search_value: rx.Var[str],
    on_change: Callable,
    on_clear: Callable | None = None,
    *,
    placeholder: str = "Search all columns...",
    width: str = "250px",
) -> rx.Component:
    """
    Create a quick filter search input for AG Grid.

    This component provides a styled search input that integrates with
    AG Grid's quickFilterText prop for instant cross-column filtering.

    Args:
        search_value: State variable containing the search text (e.g., State.search_text)
        on_change: Event handler for input changes (e.g., State.set_search)
        on_clear: Optional event handler for clear button (e.g., State.clear_search)
        placeholder: Input placeholder text
        width: Input width CSS value

    Returns:
        Search input component with optional clear button

    Usage:
        class GridState(rx.State):
            search_text: str = ""

            def set_search(self, value: str):
                self.search_text = value

            def clear_search(self):
                self.search_text = ""

        # In component:
        quick_filter_input(
            search_value=GridState.search_text,
            on_change=GridState.set_search,
            on_clear=GridState.clear_search,
        )

        # Pass to grid:
        create_standard_grid(
            ...,
            quick_filter_text=GridState.search_text,
        )
    """
    input_component = rx.input(
        placeholder=placeholder,
        value=search_value,
        on_change=on_change,
        width=width,
        size="2",
    )

    if on_clear is not None:
        return rx.hstack(
            rx.icon("search", size=16, color="gray"),
            input_component,
            rx.button(
                rx.icon("x", size=14),
                on_click=on_clear,
                size="1",
                variant="ghost",
                color_scheme="gray",
            ),
            spacing="2",
            align="center",
        )

    return rx.hstack(
        rx.icon("search", size=16, color="gray"),
        input_component,
        spacing="2",
        align="center",
    )


# =============================================================================
# CONVENIENCE EXPORTS
# =============================================================================

__all__ = [
    "create_standard_grid",
    "export_button",
    "export_buttons",
    # New grid state persistence (full: columns + filters + sort)
    "grid_state_script",
    "grid_state_buttons",
    "grid_toolbar",  # Recommended: complete toolbar with grouped buttons
    # Legacy column-only persistence (deprecated)
    "column_state_buttons",
    "get_column_state_handlers",
    "quick_filter_input",
    "get_default_export_params",
    "get_default_csv_export_params",
    "STANDARD_STATUS_BAR",
    "ENHANCED_DEFAULT_COL_DEF",
    "STANDARD_DEFAULT_COL_DEF",
    "NO_ROWS_TEMPLATE",
    "COMPACT_ROW_HEIGHT",
    "COMPACT_HEADER_HEIGHT",
]
