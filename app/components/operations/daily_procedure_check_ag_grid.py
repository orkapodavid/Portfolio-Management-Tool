"""
Daily Procedure Check AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.operations.operations_state import OperationsState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class DailyProcedureCheckGridState(rx.State):
    """State for Daily Procedure Check grid quick filter."""

    search_text: str = ""

    def set_search(self, value: str):
        self.search_text = value

    def clear_search(self):
        self.search_text = ""


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
            filter=AGFilters.date,
            min_width=100,
            pinned="left",
        ),
        ag_grid.column_def(
            field="host_run_date",
            header_name="Host Run Date",
            filter=AGFilters.date,
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
            tooltip_field="procedure_name",
        ),
        ag_grid.column_def(
            field="status",
            header_name="Status",
            filter="agSetColumnFilter",
            min_width=100,
            cell_style=_STATUS_STYLE,
        ),
        ag_grid.column_def(
            field="error_message",
            header_name="Error Message",
            filter=AGFilters.text,
            min_width=150,
            tooltip_field="error_message",
        ),
        ag_grid.column_def(
            field="frequency",
            header_name="Frequency",
            filter="agSetColumnFilter",
            min_width=100,
        ),
        ag_grid.column_def(
            field="scheduled_day",
            header_name="Scheduled Day",
            filter="agSetColumnFilter",
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

_STORAGE_KEY = "daily_procedure_check_grid_state"
_GRID_ID = "daily_procedure_check_grid"


def daily_procedure_check_ag_grid() -> rx.Component:
    """Daily Procedure Check AG-Grid component with full toolbar support."""
    from app.components.shared.ag_grid_config import (
        grid_state_script,
        grid_toolbar,
        get_default_export_params,
        get_default_csv_export_params,
    )

    return rx.vstack(
        rx.script(grid_state_script(_STORAGE_KEY, _GRID_ID)),
        grid_toolbar(
            storage_key=_STORAGE_KEY,
            page_name="daily_procedure_check",
            search_value=DailyProcedureCheckGridState.search_text,
            on_search_change=DailyProcedureCheckGridState.set_search,
            on_search_clear=DailyProcedureCheckGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=OperationsState.filtered_daily_procedures,
            column_defs=_get_column_defs(),
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params(
                "daily_procedure_check"
            ),
            default_csv_export_params=get_default_csv_export_params(
                "daily_procedure_check"
            ),
            quick_filter_text=DailyProcedureCheckGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
