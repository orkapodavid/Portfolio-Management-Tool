"""
Operation Process AG-Grid Component.

AG-Grid based implementation for operation process table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.operations.operations_state import OperationsState


# =============================================================================
# CELL STYLES
# =============================================================================

# Status style with conditional colors
_STATUS_STYLE = rx.Var(
    """(params) => {
        const status = (params.value || '');
        const colors = {
            'Active': { color: '#059669', fontWeight: '700' },
            'Inactive': { color: '#9ca3af', fontWeight: '500' },
            'Running': { color: '#d97706', fontWeight: '700' },
            'Error': { color: '#dc2626', fontWeight: '700' },
        };
        return colors[status] || { color: '#374151' };
    }"""
)


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the operation process grid."""
    return [
        ag_grid.column_def(
            field="process",
            header_name="Process",
            filter=AGFilters.text,
            min_width=200,
        ),
        ag_grid.column_def(
            field="status",
            header_name="Status",
            filter=AGFilters.text,
            min_width=120,
            cell_style=_STATUS_STYLE,
        ),
        ag_grid.column_def(
            field="last_run_time",
            header_name="Last Run Time",
            filter=AGFilters.text,
            min_width=150,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================


def operation_process_ag_grid() -> rx.Component:
    """
    Operation Process AG-Grid component.

    Displays operation processes with status coloring.
    """
    return ag_grid(
        id="operation_process_grid",
        row_data=OperationsState.filtered_operation_processes,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={
            "sortable": True,
            "resizable": True,
            "filter": True,
        },
        height="100%",
        width="100%",
    )
