"""
Reference Data AG-Grid Component.

Uses create_standard_grid factory with grid_toolbar for the Reference Data page.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from starter_app.states.market_data import MarketDataState
from starter_app.components.shared.ag_grid_config import create_standard_grid, grid_toolbar


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

# Exchange badge style
_EXCHANGE_STYLE = rx.Var(
    """(params) => ({
        backgroundColor: '#f0fdf4',
        color: '#166534',
        padding: '2px 8px',
        borderRadius: '9999px',
        fontSize: '11px',
        fontWeight: '500',
        display: 'inline-block'
    })"""
)

# Status badge style
_STATUS_STYLE = rx.Var(
    """(params) => {
        const val = (params.value || '').toLowerCase();
        const isActive = val === 'active';
        return {
            backgroundColor: isActive ? '#d1fae5' : '#fee2e2',
            color: isActive ? '#065f46' : '#991b1b',
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
    """Return column definitions for the reference data grid."""
    return [
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=110,
            pinned="left",
            cell_style=_TICKER_STYLE,
        ),
        ag_grid.column_def(
            field="name",
            header_name="Name",
            filter=AGFilters.text,
            min_width=180,
            flex=1,
        ),
        ag_grid.column_def(
            field="isin",
            header_name="ISIN",
            filter=AGFilters.text,
            min_width=140,
        ),
        ag_grid.column_def(
            field="exchange",
            header_name="Exchange",
            filter="agSetColumnFilter",
            min_width=100,
            cell_style=_EXCHANGE_STYLE,
        ),
        ag_grid.column_def(
            field="currency",
            header_name="CCY",
            filter="agSetColumnFilter",
            min_width=80,
        ),
        ag_grid.column_def(
            field="industry",
            header_name="Industry",
            filter="agSetColumnFilter",
            min_width=120,
        ),
        ag_grid.column_def(
            field="country",
            header_name="Country",
            filter="agSetColumnFilter",
            min_width=90,
        ),
        ag_grid.column_def(
            field="market_cap",
            header_name="Market Cap",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="status",
            header_name="Status",
            filter="agSetColumnFilter",
            min_width=90,
            cell_style=_STATUS_STYLE,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

_STORAGE_KEY = "reference_data_grid_state"
_GRID_ID = "reference_data_grid"


def reference_data_ag_grid() -> rx.Component:
    """Reference Data AG-Grid component with toolbar and standard enhancements."""
    return rx.vstack(
        grid_toolbar(
            storage_key=_STORAGE_KEY,
            page_name="reference_data",
            search_value=MarketDataState.ref_search_text,
            on_search_change=MarketDataState.set_ref_search,
            on_search_clear=MarketDataState.clear_ref_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
        ),
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=MarketDataState.ref_row_data,
            column_defs=_get_column_defs(),
            row_id_key="ticker",
            enable_row_numbers=True,
            enable_multi_select=True,
            quick_filter_text=MarketDataState.ref_search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
