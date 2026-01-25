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


def _get_column_defs() -> list:
    """Return column definitions for the market data grid."""
    return [
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
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
        height="calc(100vh - 300px)",
        width="100%",
    )
