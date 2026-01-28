"""
Market Data AG-Grid Component.

AG-Grid based implementation of the market data table, replacing the legacy rx.el.table.
Uses the reflex_ag_grid wrapper for enterprise features like sorting, filtering, and exports.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.market_data.market_data_state import MarketDataState


# =============================================================================
# COLUMN DEFINITIONS
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


def _get_column_defs() -> list:
    """Return column definitions for the market data grid."""
    return [
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_TICKER_STYLE,
        ),
        ag_grid.column_def(
            field="listed_shares",
            header_name="Listed Shares (mm)",
            filter=AGFilters.text,
            min_width=130,
        ),
        ag_grid.column_def(
            field="last_volume",
            header_name="Last Volume",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="last_price",
            header_name="Last Price",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="vwap_price",
            header_name="vWAP Price",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="bid",
            header_name="Bid",
            filter=AGFilters.text,
            min_width=80,
        ),
        ag_grid.column_def(
            field="ask",
            header_name="Ask",
            filter=AGFilters.text,
            min_width=80,
        ),
        ag_grid.column_def(
            field="chg_1d_pct",
            header_name="1D Change %",
            filter=AGFilters.text,
            min_width=110,
            cell_style=_CHANGE_STYLE,
        ),
        ag_grid.column_def(
            field="implied_vol_pct",
            header_name="Implied Vol %",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="market_status",
            header_name="Market Status",
            filter=AGFilters.text,
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


def market_data_ag_grid() -> rx.Component:
    """
    Market Data AG-Grid component.

    Displays real-time market data with ticker prices, volumes, and status
    using AG-Grid Enterprise features.

    Features:
    - Sortable and filterable columns
    - Clickable ticker column (blue link style)
    - Color-coded 1D Change % (green/red)
    - Badge-styled Market Status
    - Dark/light theme support
    """
    return ag_grid(
        id="market_data_grid",
        row_data=MarketDataState.filtered_market_data,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={
            "sortable": True,
            "resizable": True,
            "filter": True,
        },
        quick_filter_text=MarketDataState.market_data_search,
        height="100%",
        width="100%",
    )
