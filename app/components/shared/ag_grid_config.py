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
    # Search
    search_value: rx.Var[str] | None = None,
    on_search_change: Callable | None = None,
    on_search_clear: Callable | None = None,
    # Generate dropdown (optional)
    show_generate: bool = False,
    generate_items: list[str] | None = None,
    on_generate: Callable | None = None,
    is_generate_open: rx.Var[bool] | None = None,
    on_generate_toggle: Callable | None = None,
    # Refresh button (optional)
    show_refresh: bool = False,
    on_refresh: Callable | None = None,
    is_loading: rx.Var[bool] | None = None,
    # Date picker (optional)
    show_date_picker: bool = False,
    on_date_change: Callable | None = None,
    # Export/Layout buttons
    show_excel: bool = True,
    show_save: bool = True,
    show_restore: bool = True,
    show_reset: bool = True,
    button_size: str = "2",
    grid_id: str | None = None,
    show_compact_toggle: bool = False,
) -> rx.Component:
    """
    Unified grid toolbar with search, generate, export, and layout controls.

    This is the recommended way to add a toolbar above AG Grid components.
    It combines the styling of workspace_controls with grid-specific functionality.

    Color scheme:
    - Compact Toggle: Violet (view action) -> Green when active
    - Excel: Green (data export action)
    - Save Layout: Blue (layout action, matches Restore)
    - Restore: Blue (layout action)
    - Reset: Gray (destructive/neutral)

    Visual Layout:
        [Generate] [Export▾] [↻] [🔍 Search...] [📅 Date] | [Compact] | [Excel] | [Save] [Restore] [Reset]


    Args:
        storage_key: Unique localStorage key for grid state persistence
        page_name: Name prefix for export files (e.g., "pnl_full")

        search_value: State var for search text
        on_search_change: Handler for search input changes
        on_search_clear: Handler for clearing search

        show_generate: Show Generate dropdown button
        generate_items: List of menu items for Generate dropdown
        on_generate: Handler when a generate item is clicked (receives item label)
        is_generate_open: State var for dropdown open state
        on_generate_toggle: Handler to toggle dropdown

        show_refresh: Show Refresh button
        on_refresh: Handler for refresh click
        is_loading: State var for loading spinner

        show_date_picker: Show date picker input
        on_date_change: Handler for date changes

        show_excel: Show Excel export button
        show_save: Show Save Layout button
        show_restore: Show Restore button
        show_reset: Show Reset button
        button_size: Radix button size for layout and view buttons
        grid_id: Grid ID for API calls (required for compact toggle)
        show_compact_toggle: Show compact mode toggle button


    Returns:
        Complete toolbar styled with TailwindCSS

    Usage (simple - grid-only controls):
        grid_toolbar(
            storage_key="pnl_grid_state",
            page_name="pnl_full",
            search_value=State.search_text,
            on_search_change=State.set_search,
        )

    Usage (full - with Generate and Refresh):
        grid_toolbar(
            storage_key="pnl_grid_state",
            page_name="pnl_full",
            search_value=State.search_text,
            on_search_change=State.set_search,
            show_generate=True,
            generate_items=["Generate Report", "Refresh Data"],
            on_generate=State.handle_generate,
            is_generate_open=State.is_menu_open,
            on_generate_toggle=State.toggle_menu,
            show_refresh=True,
            on_refresh=State.refresh_data,
            is_loading=State.is_loading,
        )
    """
    safe_key = storage_key.replace("-", "_")

    # =========================================================================
    # LEFT SIDE CONTROLS
    # =========================================================================
    left_controls = []

    # Generate dropdown button
    if show_generate and generate_items and on_generate and is_generate_open is not None:
        generate_btn = rx.el.div(
            rx.el.button(
                rx.el.div(
                    rx.icon("zap", size=12),
                    rx.el.span("Generate", class_name="ml-1.5"),
                    rx.icon("chevron-down", size=10, class_name="ml-1 opacity-70"),
                    class_name="flex items-center",
                ),
                on_click=on_generate_toggle,
                class_name="px-3 h-6 bg-gradient-to-r from-blue-600 to-indigo-600 text-white text-[10px] font-black uppercase tracking-widest rounded hover:shadow-md transition-all flex items-center shadow-sm",
            ),
            rx.cond(
                is_generate_open,
                rx.el.div(
                    rx.el.div(
                        class_name="fixed inset-0 z-40",
                        on_click=on_generate_toggle,
                    ),
                    rx.el.div(
                        rx.foreach(
                            generate_items,
                            lambda item: rx.el.button(
                                item,
                                on_click=lambda i=item: on_generate(i),
                                class_name="block w-full text-left px-4 py-2 text-[10px] font-bold text-gray-700 hover:bg-gray-100 hover:text-blue-600 transition-colors",
                            ),
                        ),
                        class_name="absolute top-full left-0 mt-1 w-48 bg-white rounded-md shadow-lg border border-gray-100 py-1 z-50",
                    ),
                ),
            ),
            class_name="relative",
        )
        left_controls.append(generate_btn)

    # Excel export button (styled like workspace_controls Export)
    if show_excel:
        excel_btn = rx.el.button(
            rx.el.div(
                rx.icon("file-spreadsheet", size=12),
                rx.el.span("Excel", class_name="ml-1.5"),
                class_name="flex items-center",
            ),
            on_click=rx.call_script(_get_export_excel_js(page_name)),
            class_name="px-3 h-6 bg-white border border-gray-200 text-gray-600 text-[10px] font-bold uppercase tracking-widest rounded hover:bg-gray-50 hover:text-green-600 transition-colors shadow-sm flex items-center",
        )
        left_controls.append(excel_btn)

    # Refresh button
    if show_refresh and on_refresh:
        refresh_btn = rx.el.button(
            rx.icon(
                "refresh-cw",
                size=12,
                class_name=rx.cond(
                    is_loading if is_loading is not None else False,
                    "animate-spin",
                    "",
                ),
            ),
            on_click=on_refresh,
            class_name="h-6 w-6 flex items-center justify-center bg-white border border-gray-200 text-gray-600 rounded hover:bg-gray-50 hover:text-blue-600 transition-colors shadow-sm",
        )
        left_controls.append(refresh_btn)

    # Search input
    if search_value is not None and on_search_change is not None:
        search_input = rx.el.div(
            rx.icon("search", size=12, class_name="text-gray-400 mr-1.5 shrink-0"),
            rx.el.input(
                placeholder="Search all columns...",
                value=search_value,
                on_change=on_search_change,
                class_name="bg-transparent text-[10px] font-bold outline-none w-full text-gray-700 placeholder-gray-400",
            ),
            rx.cond(
                search_value != "",
                rx.el.button(
                    rx.icon("x", size=10, class_name="text-gray-400 hover:text-gray-600"),
                    on_click=on_search_clear if on_search_clear else lambda: None,
                    class_name="p-0.5 rounded-full hover:bg-gray-100 ml-1 transition-colors",
                ),
            ),
            class_name="flex items-center bg-white border border-gray-200 rounded px-2 h-6 flex-1 max-w-[200px] shadow-sm ml-2 transition-all focus-within:border-blue-400 focus-within:ring-1 focus-within:ring-blue-100",
        )
        left_controls.append(search_input)

    # Date picker
    if show_date_picker and on_date_change:
        date_picker = rx.el.div(
            rx.icon("calendar", size=12, class_name="text-gray-500 mr-1.5"),
            rx.el.input(
                type="date",
                on_change=on_date_change,
                class_name="bg-transparent text-[10px] font-bold text-gray-600 outline-none w-24 uppercase",
            ),
            class_name="flex items-center bg-white border border-gray-200 rounded px-2 h-6 shadow-sm hover:border-blue-400 transition-colors cursor-pointer",
        )
        left_controls.append(date_picker)

    # =========================================================================
    # RIGHT SIDE CONTROLS (Layout buttons)
    # =========================================================================
    layout_buttons = []

    if show_save:
        layout_buttons.append(
            rx.el.button(
                rx.el.div(
                    rx.icon("save", size=12),
                    rx.el.span("Save", class_name="ml-1"),
                    class_name="flex items-center",
                ),
                on_click=rx.call_script(f"saveGridState_{safe_key}()"),
                class_name="px-2 h-6 bg-white border border-gray-200 text-gray-600 text-[10px] font-bold rounded hover:bg-gray-50 hover:text-blue-600 transition-colors shadow-sm flex items-center",
            )
        )

    if show_restore:
        layout_buttons.append(
            rx.el.button(
                rx.el.div(
                    rx.icon("rotate-ccw", size=12),
                    rx.el.span("Restore", class_name="ml-1"),
                    class_name="flex items-center",
                ),
                on_click=rx.call_script(f"restoreGridState_{safe_key}()"),
                class_name="px-2 h-6 bg-white border border-gray-200 text-gray-600 text-[10px] font-bold rounded hover:bg-gray-50 hover:text-blue-600 transition-colors shadow-sm flex items-center",
            )
        )

    if show_reset:
        layout_buttons.append(
            rx.el.button(
                rx.el.div(
                    rx.icon("x", size=12),
                    rx.el.span("Reset", class_name="ml-1"),
                    class_name="flex items-center",
                ),
                on_click=rx.call_script(f"resetGridState_{safe_key}()"),
                class_name="px-2 h-6 bg-white border border-gray-200 text-gray-500 text-[10px] font-bold rounded hover:bg-gray-50 hover:text-red-600 transition-colors shadow-sm flex items-center",
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
                const textSpan = btn.querySelector('span');
                if (!isCompact) {{
                    // Now compact - show active state (green/active)
                    btn.classList.remove('bg-white', 'text-gray-600', 'hover:bg-violet-50', 'hover:text-violet-600');
                    btn.classList.add('bg-violet-100', 'text-violet-700', 'border-violet-300');
                    if (textSpan) textSpan.textContent = 'Compact ✓';
                }} else {{
                    // Now normal - show default state
                    btn.classList.remove('bg-violet-100', 'text-violet-700', 'border-violet-300');
                    btn.classList.add('bg-white', 'text-gray-600', 'hover:bg-violet-50', 'hover:text-violet-600');
                    if (textSpan) textSpan.textContent = 'Compact';
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
            rx.el.button(
                rx.el.div(
                    rx.icon("rows-3", size=12),
                    rx.el.span("Compact", class_name="ml-1"),
                    class_name="flex items-center",
                ),
                id=f"compact-toggle-{grid_id}",
                on_click=rx.call_script(toggle_compact_js),
                class_name="px-2 h-6 bg-white border border-gray-200 text-gray-600 text-[10px] font-bold rounded hover:bg-violet-50 hover:text-violet-600 transition-colors shadow-sm flex items-center",
            )
        )


    # =========================================================================
    # ASSEMBLE TOOLBAR
    # =========================================================================
    right_side_items = []

    # View buttons (Compact toggle) - first on right side
    if view_buttons:
        right_side_items.extend(view_buttons)
        # Add divider if there are more items after
        if layout_buttons:
            right_side_items.append(
                rx.el.div(class_name="w-px h-4 bg-gray-300 mx-2")
            )

    if layout_buttons:
        right_side_items.extend(layout_buttons)

    return rx.el.div(
        rx.el.div(
            *left_controls,
            class_name="flex items-center gap-2 flex-1",
        ),
        rx.el.div(
            *right_side_items,
            class_name="flex items-center gap-1",
        ),
        class_name="flex items-center justify-between px-3 py-1.5 bg-[#F9F9F9] border-b border-gray-200 shrink-0 h-[40px] w-full",
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
