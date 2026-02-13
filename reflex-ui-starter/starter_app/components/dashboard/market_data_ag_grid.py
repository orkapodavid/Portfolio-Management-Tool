"""
Market Data AG-Grid Component (Dashboard Analytics).

Uses create_standard_grid factory with grid_toolbar.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from starter_app.states.dashboard import DashboardState
from starter_app.components.shared.ag_grid_config import create_standard_grid, grid_toolbar


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

# Ticker - bold blue link-style
_TICKER_STYLE = rx.Var(
    """(params) => ({
        color: '#2563eb',
        cursor: 'pointer',
        fontWeight: '600'
    })"""
)

# Change % - green for positive, red for negative
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

# Sector badge style
_SECTOR_STYLE = rx.Var(
    """(params) => ({
        backgroundColor: '#f5f3ff',
        color: '#5b21b6',
        padding: '2px 8px',
        borderRadius: '9999px',
        fontSize: '11px',
        fontWeight: '500',
        display: 'inline-block'
    })"""
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
        ),
        ag_grid.column_def(
            field="company",
            header_name="Company",
            filter=AGFilters.text,
            min_width=180,
            flex=1,
        ),
        ag_grid.column_def(
            field="sector",
            header_name="Sector",
            filter="agSetColumnFilter",
            min_width=120,
            cell_style=_SECTOR_STYLE,
        ),
        ag_grid.column_def(
            field="price",
            header_name="Price",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="change",
            header_name="Change %",
            filter=AGFilters.number,
            min_width=110,
            cell_style=_CHANGE_STYLE,
        ),
        ag_grid.column_def(
            field="volume",
            header_name="Volume",
            filter=AGFilters.number,
            min_width=120,
        ),
        ag_grid.column_def(
            field="marketCap",
            header_name="Market Cap",
            filter=AGFilters.text,
            min_width=120,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "market_data_grid_state"
_GRID_ID = "market_data_grid"


def market_data_ag_grid() -> rx.Component:
    """Market Data AG-Grid component with toolbar and standard enhancements."""
    return rx.vstack(
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
            row_data=DashboardState.row_data,
            column_defs=_get_column_defs(),
            row_id_key="ticker",
            enable_row_numbers=True,
            enable_multi_select=True,
            quick_filter_text=MarketDataGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
        on_mount=DashboardState.load_analytics_data,
    )
