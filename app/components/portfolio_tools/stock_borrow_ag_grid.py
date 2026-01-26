"""Stock Borrow AG-Grid Component."""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.portfolio_tools.portfolio_tools_state import PortfolioToolsState


def _get_column_defs() -> list:
    return [
        ag_grid.column_def(
            field="trade_date",
            header_name="Trade Date",
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
            field="jpm_req",
            header_name="JPM Request Locate",
            filter=AGFilters.text,
            min_width=140,
        ),
        ag_grid.column_def(
            field="jpm_firm",
            header_name="JPM Firm Locate",
            filter=AGFilters.text,
            min_width=130,
        ),
        ag_grid.column_def(
            field="borrow_rate",
            header_name="Borrow Rate",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="bofa_req",
            header_name="BofA Request Locate",
            filter=AGFilters.text,
            min_width=150,
        ),
        ag_grid.column_def(
            field="bofa_firm",
            header_name="BofA Firm Locate",
            filter=AGFilters.text,
            min_width=140,
        ),
    ]


def stock_borrow_ag_grid() -> rx.Component:
    return ag_grid(
        id="stock_borrow_grid",
        row_data=PortfolioToolsState.filtered_stock_borrow,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={"sortable": True, "resizable": True, "filter": True},
        height="calc(100vh - 300px)",
        width="100%",
    )
