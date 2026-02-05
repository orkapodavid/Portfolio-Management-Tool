"""
Risk Input Recon AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.reconciliation.reconciliation_state import ReconciliationState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class RiskInputReconGridState(rx.State):
    """State for Risk Input Recon grid quick filter."""

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
            field="underlying",
            header_name="Underlying",
            filter=AGFilters.text,
            min_width=100,
            tooltip_field="underlying",
        ),
        ag_grid.column_def(
            field="sec_type",
            header_name="Sec Type",
            filter="agSetColumnFilter",
            min_width=90,
        ),
        ag_grid.column_def(
            field="spot_mc",
            header_name="Spot (MC)",
            filter=AGFilters.number,
            min_width=90,
        ),
        ag_grid.column_def(
            field="spot_ppd",
            header_name="Spot (PPD)",
            filter=AGFilters.number,
            min_width=90,
        ),
        ag_grid.column_def(
            field="position",
            header_name="Position",
            filter=AGFilters.number,
            min_width=90,
        ),
        ag_grid.column_def(
            field="value_mc",
            header_name="Value (MC)",
            filter=AGFilters.number,
            min_width=90,
        ),
        ag_grid.column_def(
            field="value_ppd",
            header_name="Value (PPD)",
            filter=AGFilters.number,
            min_width=90,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "risk_input_recon_grid_state"
_GRID_ID = "risk_input_recon_grid"


def risk_input_recon_ag_grid() -> rx.Component:
    """Risk Input Recon AG-Grid component with full toolbar support."""
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
            page_name="risk_input_recon",
            search_value=RiskInputReconGridState.search_text,
            on_search_change=RiskInputReconGridState.set_search,
            on_search_clear=RiskInputReconGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            # Force refresh pattern
            show_refresh=True,
            on_refresh=ReconciliationState.force_refresh_risk_input_recon,
            is_loading=ReconciliationState.is_loading_risk_input_recon,
            last_updated=ReconciliationState.risk_input_recon_last_updated,
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=ReconciliationState.filtered_risk_input_recon,
            column_defs=_get_column_defs(),
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("risk_input_recon"),
            default_csv_export_params=get_default_csv_export_params("risk_input_recon"),
            quick_filter_text=RiskInputReconGridState.search_text,
            row_id_key="id",
            enable_cell_flash=True,
            loading=ReconciliationState.is_loading_risk_input_recon,
            overlay_loading_template="<span class='ag-overlay-loading-center'>Refreshing data...</span>",
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
