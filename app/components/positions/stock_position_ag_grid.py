"""
Stock Position AG-Grid Component.

AG-Grid based implementation for stock position table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.positions.positions_state import PositionsState


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the stock position grid."""
    return [
        ag_grid.column_def(
            field="trade_date",
            header_name="Trade Date",
            filter=AGFilters.text,
            min_width=100,
        ),
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
            field="currency",
            header_name="Currency",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="account_id",
            header_name="Account ID",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="position_location",
            header_name="Position Location",
            filter=AGFilters.text,
            min_width=130,
        ),
        ag_grid.column_def(
            field="notional",
            header_name="Notional",
            filter=AGFilters.text,
            min_width=100,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================


def stock_position_ag_grid() -> rx.Component:
    """
    Stock Position AG-Grid component.

    Displays stock position data.
    """
    return ag_grid(
        id="stock_position_grid",
        row_data=PositionsState.filtered_stock_positions,
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
