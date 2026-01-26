"""
Trade Summary AG-Grid Component.

AG-Grid based implementation for trade summary table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.positions.positions_state import PositionsState


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the trade summary grid."""
    return [
        ag_grid.column_def(
            field="deal_num",
            header_name="Deal Num",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="detail_id",
            header_name="Detail ID",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
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
            field="account_id",
            header_name="Account ID",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="company_name",
            header_name="Company Name",
            filter=AGFilters.text,
            min_width=150,
        ),
        ag_grid.column_def(
            field="sec_id",
            header_name="SecID",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="sec_type",
            header_name="Sec Type",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="subtype",
            header_name="Subtype",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="currency",
            header_name="Currency",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="closing_date",
            header_name="Closing Date",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="divisor",
            header_name="Divisor",
            filter=AGFilters.text,
            min_width=80,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================


def trade_summary_ag_grid() -> rx.Component:
    """
    Trade Summary AG-Grid component.

    Displays trade summary data.
    """
    return ag_grid(
        id="trade_summary_grid",
        row_data=PositionsState.filtered_trade_summaries,
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
