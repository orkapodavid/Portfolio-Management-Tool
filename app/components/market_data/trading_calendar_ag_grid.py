"""
Trading Calendar AG-Grid Component.

AG-Grid based implementation for trading calendar, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.market_data.market_data_state import MarketDataState


# =============================================================================
# CELL STYLES
# =============================================================================

# Market status style - green for open, red for closed
_MARKET_STATUS_STYLE = rx.Var(
    """(params) => {
        const val = (params.value || '').toLowerCase();
        const isOpen = val.includes('open') || val === 'o' || val === '1';
        if (!val || val === '-') return {};
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
    """Return column definitions for the trading calendar grid."""
    return [
        ag_grid.column_def(
            field="trade_date",
            header_name="Trade Date",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="day_of_week",
            header_name="Day of Week",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="usa",
            header_name="USA",
            filter=AGFilters.text,
            min_width=80,
            cell_style=_MARKET_STATUS_STYLE,
        ),
        ag_grid.column_def(
            field="hkg",
            header_name="HKG",
            filter=AGFilters.text,
            min_width=80,
            cell_style=_MARKET_STATUS_STYLE,
        ),
        ag_grid.column_def(
            field="jpn",
            header_name="JPN",
            filter=AGFilters.text,
            min_width=80,
            cell_style=_MARKET_STATUS_STYLE,
        ),
        ag_grid.column_def(
            field="aus",
            header_name="AUS",
            filter=AGFilters.text,
            min_width=80,
            cell_style=_MARKET_STATUS_STYLE,
        ),
        ag_grid.column_def(
            field="nzl",
            header_name="NZL",
            filter=AGFilters.text,
            min_width=80,
            cell_style=_MARKET_STATUS_STYLE,
        ),
        ag_grid.column_def(
            field="kor",
            header_name="KOR",
            filter=AGFilters.text,
            min_width=80,
            cell_style=_MARKET_STATUS_STYLE,
        ),
        ag_grid.column_def(
            field="chn",
            header_name="CHN",
            filter=AGFilters.text,
            min_width=80,
            cell_style=_MARKET_STATUS_STYLE,
        ),
        ag_grid.column_def(
            field="twn",
            header_name="TWN",
            filter=AGFilters.text,
            min_width=80,
            cell_style=_MARKET_STATUS_STYLE,
        ),
        ag_grid.column_def(
            field="ind",
            header_name="IND",
            filter=AGFilters.text,
            min_width=80,
            cell_style=_MARKET_STATUS_STYLE,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================


def trading_calendar_ag_grid() -> rx.Component:
    """
    Trading Calendar AG-Grid component.

    Displays trading calendar with date and market open/close status
    for USA, HKG, JPN, AUS, NZL, KOR, CHN, TWN, IND markets.
    """
    return ag_grid(
        id="trading_calendar_grid",
        row_data=MarketDataState.trading_calendar,
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
