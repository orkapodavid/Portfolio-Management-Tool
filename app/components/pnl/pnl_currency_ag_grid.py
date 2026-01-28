"""
PnL Currency AG-Grid Component.

AG-Grid based implementation for PnL currency table, replacing legacy rx.el.table.
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
    """Return column definitions for the PnL currency grid."""
    return [
        ag_grid.column_def(
            field="trade_date",
            header_name="Trade Date",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="currency",
            header_name="Currency",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="fx_rate",
            header_name="FX Rate",
            filter=AGFilters.text,
            min_width=90,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="fx_rate_t_1",
            header_name="FX Rate (T-1)",
            filter=AGFilters.text,
            min_width=110,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="fx_rate_change",
            header_name="FX Rate Change",
            filter=AGFilters.text,
            min_width=120,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="ccy_exposure",
            header_name="CCY Exposure",
            filter=AGFilters.text,
            min_width=110,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="usd_exposure",
            header_name="USD Exposure",
            filter=AGFilters.text,
            min_width=110,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="pos_ccy_expo",
            header_name="POS CCY Expo",
            filter=AGFilters.text,
            min_width=110,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="ccy_hedged_pnl",
            header_name="CCY Hedged PnL",
            filter=AGFilters.text,
            min_width=120,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="pos_ccy_pnl",
            header_name="POS CCY PnL",
            filter=AGFilters.text,
            min_width=110,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="net_ccy",
            header_name="Net CC",
            filter=AGFilters.text,
            min_width=90,
            cell_style=_VALUE_STYLE,
        ),
        ag_grid.column_def(
            field="pos_c_truncated",
            header_name="POS C (truncated)",
            filter=AGFilters.text,
            min_width=130,
            cell_style=_VALUE_STYLE,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================


def pnl_currency_ag_grid() -> rx.Component:
    """
    PnL Currency AG-Grid component.

    Displays PnL currency data with color-coded values.
    """
    return ag_grid(
        id="pnl_currency_grid",
        row_data=PnLState.filtered_pnl_currency,
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
