"""Excess Amount AG-Grid Component."""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.portfolio_tools.portfolio_tools_state import PortfolioToolsState


def _get_column_defs() -> list:
    return [
        ag_grid.column_def(
            field="deal_num",
            header_name="Deal Num",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="underlying",
            header_name="Underlying",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="ticker", header_name="Ticker", filter=AGFilters.text, min_width=100
        ),
        ag_grid.column_def(
            field="company_name",
            header_name="Company Name",
            filter=AGFilters.text,
            min_width=150,
        ),
        ag_grid.column_def(
            field="warrants",
            header_name="Warrants",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="excess_amount",
            header_name="Excess Amount",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="threshold",
            header_name="Excess Amount Threshold",
            filter=AGFilters.text,
            min_width=170,
        ),
        ag_grid.column_def(
            field="cb_redeem",
            header_name="CB Redeem/Converted Amt",
            filter=AGFilters.text,
            min_width=180,
        ),
        ag_grid.column_def(
            field="redeem",
            header_name="Redeem/Converted Amt",
            filter=AGFilters.text,
            min_width=160,
        ),
    ]


def excess_amount_ag_grid() -> rx.Component:
    return ag_grid(
        id="excess_amount_grid",
        row_data=PortfolioToolsState.filtered_excess_amount,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={"sortable": True, "resizable": True, "filter": True},
        height="100%",
        width="100%",
    )
