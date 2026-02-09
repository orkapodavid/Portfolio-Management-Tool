"""
Export parameter generators and JavaScript helpers for AG Grid exports.

Provides default Excel/CSV export params with timestamped filenames
and conditional row filtering (selected rows only, or all if no selection).
"""

import reflex as rx


# =============================================================================
# INTERNAL HELPERS
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


# =============================================================================
# PUBLIC API
# =============================================================================


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
# JAVASCRIPT FOR DIRECT EXCEL EXPORT (used by toolbar)
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
