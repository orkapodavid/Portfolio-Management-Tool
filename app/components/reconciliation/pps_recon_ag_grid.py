"""
PPS Recon AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.reconciliation.reconciliation_state import ReconciliationState
from app.components.shared.ag_grid_config import (
    create_standard_grid,
    FILTER_LABEL_CLASS,
    FILTER_INPUT_CLASS,
)


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class PpsReconGridState(rx.State):
    """State for PPS Recon grid quick filter."""

    search_text: str = ""

    def set_search(self, value: str):
        self.search_text = value

    def clear_search(self):
        self.search_text = ""


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    return [
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
            pinned="left",
            tooltip_field="ticker",
        ),
        ag_grid.column_def(
            field="value_date",
            header_name="Value Date",
            filter=AGFilters.date,
            min_width=100,
        ),
        ag_grid.column_def(
            field="trade_date",
            header_name="Trade Date",
            filter=AGFilters.date,
            min_width=100,
        ),
        ag_grid.column_def(
            field="underlying",
            header_name="Underlying",
            filter=AGFilters.text,
            min_width=100,
            tooltip_field="underlying",
        ),
        ag_grid.column_def(
            field="code",
            header_name="Code",
            filter=AGFilters.text,
            min_width=80,
        ),
        ag_grid.column_def(
            field="company_name",
            header_name="Company Name",
            filter=AGFilters.text,
            min_width=150,
            tooltip_field="company_name",
        ),
        ag_grid.column_def(
            field="sec_type",
            header_name="Sec Type",
            filter="agSetColumnFilter",
            min_width=90,
        ),
        ag_grid.column_def(
            field="pos_loc",
            header_name="Pos Loc",
            filter="agSetColumnFilter",
            min_width=80,
        ),
        ag_grid.column_def(
            field="account",
            header_name="Account",
            filter="agSetColumnFilter",
            min_width=100,
        ),
    ]


# =============================================================================
# POSITION DATE FILTER BAR
# =============================================================================


def _position_date_bar() -> rx.Component:
    """Position date selector bar."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("calendar", size=14, class_name="text-gray-400"),
                rx.el.span("POSITION DATE", class_name=FILTER_LABEL_CLASS),
                rx.el.input(
                    type="date",
                    value=ReconciliationState.pps_recon_position_date,
                    on_change=ReconciliationState.set_pps_recon_position_date,
                    class_name=f"{FILTER_INPUT_CLASS} w-[150px]",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        class_name=(
            "w-full px-3 py-2 bg-gradient-to-r from-gray-50/80 to-slate-50/80 "
            "border-b border-gray-100 backdrop-blur-sm"
        ),
    )


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "pps_recon_grid_state"
_GRID_ID = "pps_recon_grid"


def pps_recon_ag_grid() -> rx.Component:
    """PPS Recon AG-Grid component with full toolbar support."""
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
            page_name="pps_recon",
            search_value=PpsReconGridState.search_text,
            on_search_change=PpsReconGridState.set_search,
            on_search_clear=PpsReconGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            # Force refresh pattern
            show_refresh=True,
            on_refresh=ReconciliationState.force_refresh_pps_recon,
            is_loading=ReconciliationState.is_loading_pps_recon,
            last_updated=ReconciliationState.pps_recon_last_updated,
        ),
        _position_date_bar(),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=ReconciliationState.filtered_pps_recon,
            column_defs=_get_column_defs(),
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("pps_recon"),
            default_csv_export_params=get_default_csv_export_params("pps_recon"),
            quick_filter_text=PpsReconGridState.search_text,
            row_id_key="id",
            enable_cell_flash=True,
            loading=ReconciliationState.is_loading_pps_recon,
            overlay_loading_template="<span class='ag-overlay-loading-center'>Refreshing data...</span>",
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
