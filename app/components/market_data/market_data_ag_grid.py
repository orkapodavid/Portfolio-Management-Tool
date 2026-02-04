"""
Market Data AG-Grid Component.

Migrated to use create_standard_grid factory with cell flash and full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.market_data.market_data_state import MarketDataState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class MarketDataGridState(rx.State):
    """State for Market Data grid quick filter."""

    search_text: str = ""

    def set_search(self, value: str):
        self.search_text = value

    def clear_search(self):
        self.search_text = ""


# =============================================================================
# CELL STYLES
# =============================================================================

# Cell style for Ticker - blue link style
_TICKER_STYLE = rx.Var(
    """(params) => ({
        color: '#2563eb',
        cursor: 'pointer',
        fontWeight: '600'
    })"""
)

# Cell style for 1D Change % - green for positive, red for negative
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

# Cell style for Market Status - badge style with background
_STATUS_STYLE = rx.Var(
    """(params) => {
        const val = (params.value || '').toLowerCase();
        const isOpen = val.includes('open');
        return {
            backgroundColor: isOpen ? '#d1fae5' : '#fee2e2',
            color: isOpen ? '#065f46' : '#991b1b',
            padding: '2px 8px',
            borderRadius: '9999px',
            fontSize: '11px',
            fontWeight: '500',
            display: 'inline-block'
        };
    }"""
)


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the market data grid."""
    return [
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
            pinned="left",
            cell_style=_TICKER_STYLE,
            tooltip_field="ticker",
        ),
        ag_grid.column_def(
            field="listed_shares",
            header_name="Listed Shares (mm)",
            filter=AGFilters.number,
            min_width=130,
        ),
        ag_grid.column_def(
            field="last_volume",
            header_name="Last Volume",
            filter=AGFilters.number,
            min_width=110,
        ),
        ag_grid.column_def(
            field="last_price",
            header_name="Last Price",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="vwap_price",
            header_name="vWAP Price",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="bid",
            header_name="Bid",
            filter=AGFilters.number,
            min_width=80,
        ),
        ag_grid.column_def(
            field="ask",
            header_name="Ask",
            filter=AGFilters.number,
            min_width=80,
        ),
        ag_grid.column_def(
            field="chg_1d_pct",
            header_name="1D Change %",
            filter=AGFilters.number,
            min_width=110,
            cell_style=_CHANGE_STYLE,
        ),
        ag_grid.column_def(
            field="implied_vol_pct",
            header_name="Implied Vol %",
            filter=AGFilters.number,
            min_width=110,
        ),
        ag_grid.column_def(
            field="market_status",
            header_name="Market Status",
            filter="agSetColumnFilter",
            min_width=120,
            cell_style=_STATUS_STYLE,
        ),
        ag_grid.column_def(
            field="created_by",
            header_name="Created by",
            filter=AGFilters.text,
            min_width=100,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "market_data_grid_state"
_GRID_ID = "market_data_grid"


def market_data_ag_grid() -> rx.Component:
    """Market Data AG-Grid component with cell flash and full toolbar support."""
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
            page_name="market_data",
            search_value=MarketDataGridState.search_text,
            on_search_change=MarketDataGridState.set_search,
            on_search_clear=MarketDataGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=MarketDataState.filtered_market_data,
            column_defs=_get_column_defs(),
            enable_cell_flash=True,  # Enable for market data
            enable_row_numbers=True,
            enable_multi_select=True,
            default_excel_export_params=get_default_export_params("market_data"),
            default_csv_export_params=get_default_csv_export_params("market_data"),
            quick_filter_text=MarketDataGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
