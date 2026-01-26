"""
Daily Procedure Check AG-Grid Component.

AG-Grid based implementation for daily procedure check table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.operations.operations_state import OperationsState


# =============================================================================
# CELL STYLES
# =============================================================================

# Status badge style for Success/Failed/Active/Inactive
_STATUS_STYLE = rx.Var(
    """(params) => {
        const status = (params.value || '').toLowerCase();
        const colors = {
            'success': { backgroundColor: '#dcfce7', color: '#166534' },
            'filled': { backgroundColor: '#dcfce7', color: '#166534' },
            'active': { backgroundColor: '#dcfce7', color: '#166534' },
            'failed': { backgroundColor: '#fee2e2', color: '#dc2626' },
            'error': { backgroundColor: '#fee2e2', color: '#dc2626' },
            'inactive': { backgroundColor: '#f3f4f6', color: '#6b7280' },
            'running': { backgroundColor: '#fef3c7', color: '#d97706' },
            'warning': { backgroundColor: '#fef3c7', color: '#d97706' },
        };
        return {
            ...(colors[status] || { backgroundColor: '#dbeafe', color: '#2563eb' }),
            padding: '2px 8px',
            borderRadius: '9999px',
            fontSize: '9px',
            fontWeight: '700',
            textTransform: 'uppercase',
        };
    }"""
)


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the daily procedure check grid."""
    return [
        ag_grid.column_def(
            field="check_date",
            header_name="Check Date",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="host_run_date",
            header_name="Host Run Date",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="scheduled_time",
            header_name="Scheduled Time",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="procedure_name",
            header_name="Procedure Name",
            filter=AGFilters.text,
            min_width=150,
        ),
        ag_grid.column_def(
            field="status",
            header_name="Status",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_STATUS_STYLE,
        ),
        ag_grid.column_def(
            field="error_message",
            header_name="Error Message",
            filter=AGFilters.text,
            min_width=150,
        ),
        ag_grid.column_def(
            field="frequency",
            header_name="Frequency",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="scheduled_day",
            header_name="Scheduled Day",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="created_by",
            header_name="Created By",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="created_time",
            header_name="Created Time",
            filter=AGFilters.text,
            min_width=110,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================


def daily_procedure_check_ag_grid() -> rx.Component:
    """
    Daily Procedure Check AG-Grid component.

    Displays daily procedure checks with status badges.
    """
    return ag_grid(
        id="daily_procedure_check_grid",
        row_data=OperationsState.filtered_daily_procedures,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={
            "sortable": True,
            "resizable": True,
            "filter": True,
        },
        height="calc(100vh - 300px)",
        width="100%",
    )
