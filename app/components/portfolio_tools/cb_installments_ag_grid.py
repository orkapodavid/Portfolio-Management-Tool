"""CB Installments AG-Grid Component."""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.portfolio_tools.portfolio_tools_state import PortfolioToolsState


def _get_column_defs() -> list:
    return [
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
            field="currency",
            header_name="Currency",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="installment_date",
            header_name="Installment Date",
            filter=AGFilters.text,
            min_width=130,
        ),
        ag_grid.column_def(
            field="total_amount",
            header_name="Total Amount",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="outstanding",
            header_name="Outstanding Amount",
            filter=AGFilters.text,
            min_width=150,
        ),
        ag_grid.column_def(
            field="redeemed",
            header_name="Redeemed Amount",
            filter=AGFilters.text,
            min_width=140,
        ),
        ag_grid.column_def(
            field="deferred",
            header_name="Deferred Amount",
            filter=AGFilters.text,
            min_width=130,
        ),
        ag_grid.column_def(
            field="converted",
            header_name="Converted Amount",
            filter=AGFilters.text,
            min_width=140,
        ),
        ag_grid.column_def(
            field="installment_amount",
            header_name="Installment Amount",
            filter=AGFilters.text,
            min_width=150,
        ),
        ag_grid.column_def(
            field="period", header_name="Period", filter=AGFilters.text, min_width=80
        ),
    ]


def cb_installments_ag_grid() -> rx.Component:
    return ag_grid(
        id="cb_installments_grid",
        row_data=PortfolioToolsState.filtered_cb_installments,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={"sortable": True, "resizable": True, "filter": True},
        height="100%",
        width="100%",
    )
