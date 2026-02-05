"""
Historical Data AG-Grid Component.

Migrated to use create_standard_grid factory with cell flash and full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.market_data.market_data_state import MarketDataState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class HistoricalDataGridState(rx.State):
    """State for Historical Data grid quick filter only."""

    search_text: str = ""

    def set_search(self, value: str):
        self.search_text = value

    def clear_search(self):
        self.search_text = ""


# =============================================================================
# CELL STYLES
# =============================================================================

# Ticker style - blue link
_TICKER_STYLE = rx.Var(
    """(params) => ({
        color: '#2563eb',
        cursor: 'pointer',
        fontWeight: '600'
    })"""
)

# Change % style - green for positive, red for negative
_CHANGE_STYLE = rx.Var(
    """(params) => {
        const val = parseFloat(params.value);
        if (isNaN(val)) return {};
        return {
            color: val >= 0 ? '#059669' : '#dc2626',
            fontWeight: '500'
        };
    }"""
)


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the historical data grid."""
    return [
        ag_grid.column_def(
            field="trade_date",
            header_name="Trade Date",
            filter=AGFilters.date,
            min_width=110,
            pinned="left",
        ),
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_TICKER_STYLE,
            tooltip_field="ticker",
        ),
        ag_grid.column_def(
            field="vwap_price",
            header_name="vWAP Price",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="last_price",
            header_name="Last Price",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="last_volume",
            header_name="Last Volume",
            filter=AGFilters.number,
            min_width=110,
        ),
        ag_grid.column_def(
            field="chg_1d_pct",
            header_name="1D Change %",
            filter=AGFilters.number,
            min_width=110,
            cell_style=_CHANGE_STYLE,
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
            min_width=120,
        ),
        ag_grid.column_def(
            field="updated_by",
            header_name="Updated By",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="update",
            header_name="Update",
            filter=AGFilters.text,
            min_width=120,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "historical_data_grid_state"
_GRID_ID = "historical_data_grid"


def historical_data_ag_grid() -> rx.Component:
    """Historical Data AG-Grid component with cell flash and full toolbar support."""
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
            page_name="historical_data",
            search_value=HistoricalDataGridState.search_text,
            on_search_change=HistoricalDataGridState.set_search,
            on_search_clear=HistoricalDataGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            # Status bar — timestamp from mixin, toggle from mixin
            last_updated=MarketDataState.historical_data_last_updated,
            auto_refresh=MarketDataState.historical_auto_refresh,
            on_auto_refresh_toggle=MarketDataState.toggle_historical_auto_refresh,
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=MarketDataState.filtered_historical_data,
            column_defs=_get_column_defs(),
            row_id_key="ticker",  # CRITICAL: enables delta updates
            enable_cell_flash=True,  # Enable for market data
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("historical_data"),
            default_csv_export_params=get_default_csv_export_params("historical_data"),
            quick_filter_text=HistoricalDataGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
        on_mount=MarketDataState.start_historical_auto_refresh,
    )
