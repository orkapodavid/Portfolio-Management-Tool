"""
PnL Recon AG-Grid Component.

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


class PnlReconGridState(rx.State):
    """State for PnL Recon grid quick filter."""

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
            field="underlying",
            header_name="Underlying",
            filter=AGFilters.text,
            min_width=100,
            pinned="left",
            tooltip_field="underlying",
        ),
        ag_grid.column_def(
            field="trade_date",
            header_name="Trade Date",
            filter=AGFilters.date,
            min_width=100,
        ),
        ag_grid.column_def(
            field="report_date",
            header_name="Report Date",
            filter=AGFilters.date,
            min_width=100,
        ),
        ag_grid.column_def(
            field="deal_num",
            header_name="Deal Num",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="row_index",
            header_name="Row Index",
            filter=AGFilters.number,
            min_width=90,
        ),
        ag_grid.column_def(
            field="pos_loc",
            header_name="Pos Loc",
            filter="agSetColumnFilter",
            min_width=80,
        ),
        ag_grid.column_def(
            field="stock_sec_id",
            header_name="Stock SecID",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="warrant_sec_id",
            header_name="Warrant SecID",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="bond_sec_id",
            header_name="Bond SecID",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="stock_position",
            header_name="Stock Position",
            filter=AGFilters.number,
            min_width=110,
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
                    value=ReconciliationState.pnl_recon_position_date,
                    on_change=ReconciliationState.set_pnl_recon_position_date,
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

_STORAGE_KEY = "pnl_recon_grid_state"
_GRID_ID = "pnl_recon_grid"


def pnl_recon_ag_grid() -> rx.Component:
    """PnL Recon AG-Grid component with full toolbar support."""
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
            page_name="pnl_recon",
            search_value=PnlReconGridState.search_text,
            on_search_change=PnlReconGridState.set_search,
            on_search_clear=PnlReconGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            # Force refresh pattern
            show_refresh=True,
            on_refresh=ReconciliationState.force_refresh_pnl_recon,
            is_loading=ReconciliationState.is_loading_pnl_recon,
            last_updated=ReconciliationState.pnl_recon_last_updated,
        ),
        _position_date_bar(),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=ReconciliationState.filtered_pnl_recon,
            column_defs=_get_column_defs(),
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("pnl_recon"),
            default_csv_export_params=get_default_csv_export_params("pnl_recon"),
            quick_filter_text=PnlReconGridState.search_text,
            row_id_key="id",
            enable_cell_flash=True,
            loading=ReconciliationState.is_loading_pnl_recon,
            overlay_loading_template="<span class='ag-overlay-loading-center'>Refreshing data...</span>",
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
