"""
Historical Data AG-Grid Component.

AG-Grid based implementation for historical price data, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.market_data.market_data_state import MarketDataState


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
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_TICKER_STYLE,
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


def historical_data_ag_grid() -> rx.Component:
    """
    Historical Data AG-Grid component.

    Displays historical price and volume data with trade date, ticker,
    prices, change percentage, and audit timestamps.
    """
    return ag_grid(
        id="historical_data_grid",
        row_data=MarketDataState.filtered_historical_data,
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
