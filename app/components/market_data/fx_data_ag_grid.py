"""
FX Data AG-Grid Component.

AG-Grid based implementation for FX rate data, replacing legacy rx.el.table.
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


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the FX data grid."""
    return [
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_TICKER_STYLE,
        ),
        ag_grid.column_def(
            field="last_price",
            header_name="Last Price",
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
            field="created_by",
            header_name="Created by",
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
            header_name="Updated by",
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


def fx_data_ag_grid() -> rx.Component:
    """
    FX Data AG-Grid component.

    Displays foreign exchange rate data with ticker, bid/ask prices,
    and audit timestamps using AG-Grid Enterprise features.
    """
    return ag_grid(
        id="fx_data_grid",
        row_data=MarketDataState.filtered_fx_data,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={
            "sortable": True,
            "resizable": True,
            "filter": True,
        },
        height="100%",
        width="100%",
    )
