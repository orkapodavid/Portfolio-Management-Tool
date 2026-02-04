"""
Ticker Data AG-Grid Component.

Migrated to use create_standard_grid factory with full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.instruments.instrument_state import InstrumentState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class TickerDataGridState(rx.State):
    """State for Ticker Data grid quick filter."""

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
            field="currency",
            header_name="Currency",
            filter="agSetColumnFilter",  # Categorical
            min_width=90,
        ),
        ag_grid.column_def(
            field="fx_rate",
            header_name="FX Rate",
            filter=AGFilters.number,
            min_width=90,
        ),
        ag_grid.column_def(
            field="sector",
            header_name="Sector",
            filter="agSetColumnFilter",  # Categorical
            min_width=100,
        ),
        ag_grid.column_def(
            field="company",
            header_name="Company",
            filter=AGFilters.text,
            min_width=150,
            tooltip_field="company",
        ),
        ag_grid.column_def(
            field="po_lead_manager",
            header_name="PO Lead Manager",
            filter=AGFilters.text,
            min_width=130,
            tooltip_field="po_lead_manager",
        ),
        ag_grid.column_def(
            field="fmat_cap",
            header_name="FMat Cap",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="smkt_cap",
            header_name="SMkt Cap",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="chg_1d_pct",
            header_name="1D%",
            filter=AGFilters.number,
            min_width=80,
        ),
        ag_grid.column_def(
            field="dtl",
            header_name="DTL",
            filter=AGFilters.text,
            min_width=80,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "ticker_data_grid_state"
_GRID_ID = "ticker_data_grid"


def ticker_data_ag_grid() -> rx.Component:
    """Ticker Data AG-Grid component with full toolbar support."""
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
            page_name="ticker_data",
            search_value=TickerDataGridState.search_text,
            on_search_change=TickerDataGridState.set_search,
            on_search_clear=TickerDataGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=InstrumentState.filtered_ticker_data,
            column_defs=_get_column_defs(),
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("ticker_data"),
            default_csv_export_params=get_default_csv_export_params("ticker_data"),
            quick_filter_text=TickerDataGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
