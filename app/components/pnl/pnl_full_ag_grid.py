"""
PnL Full AG-Grid Component.

AG-Grid based implementation for PnL full table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.pnl.pnl_state import PnLState


# =============================================================================
# CELL STYLES
# =============================================================================

# Value style - green for positive, red for negative
_VALUE_STYLE = rx.Var(
    """(params) => {
        const val = String(params.value || '');
        const isNegative = val.startsWith('-') || val.startsWith('(');
        return {
            color: isNegative ? '#dc2626' : '#059669',
            fontWeight: '700',
            fontFamily: 'monospace'
        };
    }"""
)


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the PnL full grid."""
    return [
        ag_grid.column_def(
            field="trade_date",
            header_name="Trade Date",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="underlying",
            header_name="Underlying",
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
            field="pnl_ytd",
            header_name="PnL YTD",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="pnl_chg_1d",
            header_name="PnL Chg 1D",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="pnl_chg_1w",
            header_name="PnL Chg 1W",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="pnl_chg_1m",
            header_name="PnL Chg 1M",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="pnl_chg_pct_1d",
            header_name="PnL Chg% 1D",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="pnl_chg_pct_1w",
            header_name="PnL Chg% 1W",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="pnl_chg_pct_1m",
            header_name="PnL Chg% 1M",
            filter=AGFilters.text,
            min_width=100,
            cell_style=_VALUE_STYLE,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================


def pnl_full_ag_grid() -> rx.Component:
    """
    PnL Full AG-Grid component.

    Displays full PnL data with color-coded values.
    """
    return ag_grid(
        id="pnl_full_grid",
        row_data=PnLState.filtered_pnl_full,
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
