"""
Operation Process AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.operations.operations_state import OperationsState
from app.components.shared.ag_grid_config import (
    create_standard_grid,
    build_context_menu,
    context_menu_dispatch_input,
)


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class OperationProcessGridState(rx.State):
    """State for Operation Process grid quick filter."""

    search_text: str = ""

    def set_search(self, value: str):
        self.search_text = value

    def clear_search(self):
        self.search_text = ""


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
            pinned="left",
            tooltip_field="process",
        ),
        ag_grid.column_def(
            field="status",
            header_name="Status",
            filter="agSetColumnFilter",
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
# CONTEXT MENU
# =============================================================================

_CTX_MENU_ID = "op_process_ctx"

_CONTEXT_MENU = build_context_menu(
    target_id=_CTX_MENU_ID,
    items=[
        {"name": "Rerun", "icon": "🔄"},
        {"name": "Kill", "icon": "🛑"},
    ],
)


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "operation_process_grid_state"
_GRID_ID = "operation_process_grid"


def operation_process_ag_grid() -> rx.Component:
    """Operation Process AG-Grid component with full toolbar support."""
    from app.components.shared.ag_grid_config import (
        grid_state_script,
        grid_toolbar,
        get_default_export_params,
        get_default_csv_export_params,
    )

    return rx.vstack(
        # Hidden input for context menu dispatch bridge
        context_menu_dispatch_input(
            target_id=_CTX_MENU_ID,
            on_action=OperationsState.handle_context_menu_action,
        ),
        rx.script(grid_state_script(_STORAGE_KEY, _GRID_ID)),
        grid_toolbar(
            storage_key=_STORAGE_KEY,
            page_name="operation_process",
            search_value=OperationProcessGridState.search_text,
            on_search_change=OperationProcessGridState.set_search,
            on_search_clear=OperationProcessGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            last_updated=OperationsState.operation_processes_last_updated,
            show_refresh=True,
            on_refresh=OperationsState.force_refresh_operation_processes,
            is_loading=OperationsState.is_loading_operation_processes,
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=OperationsState.operation_processes,
            column_defs=_get_column_defs(),
            row_id_key="id",
            loading=OperationsState.is_loading_operation_processes,
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("operation_process"),
            default_csv_export_params=get_default_csv_export_params(
                "operation_process"
            ),
            quick_filter_text=OperationProcessGridState.search_text,
            get_context_menu_items=_CONTEXT_MENU,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
