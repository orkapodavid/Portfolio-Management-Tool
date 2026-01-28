"""
Market Hours AG-Grid Component.

AG-Grid based implementation for market hours data, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.market_data.market_data_state import MarketDataState


# =============================================================================
# CELL STYLES
# =============================================================================

# Is Open style - badge
_IS_OPEN_STYLE = rx.Var(
    """(params) => {
        const val = (params.value || '').toLowerCase();
        const isOpen = val === 'yes' || val === 'true' || val === '1' || val === 'open';
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
    """Return column definitions for the market hours grid."""
    return [
        ag_grid.column_def(
            field="market",
            header_name="Market",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="session",
            header_name="Session",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="local_time",
            header_name="Local Time",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="session_period",
            header_name="Session Period",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="is_open",
            header_name="Is Open?",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_IS_OPEN_STYLE,
        ),
        ag_grid.column_def(
            field="timezone",
            header_name="Timezone",
            filter=AGFilters.text,
            min_width=100,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================


def market_hours_ag_grid() -> rx.Component:
    """
    Market Hours AG-Grid component.

    Displays market session hours, local time, session period,
    open status, and timezone information.
    """
    return ag_grid(
        id="market_hours_grid",
        row_data=MarketDataState.market_hours,
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
