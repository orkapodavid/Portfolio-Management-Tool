"""Reset Dates AG-Grid Component."""

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
            field="company_name",
            header_name="Company Name",
            filter=AGFilters.text,
            min_width=150,
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
            field="trade_date",
            header_name="Trade Date",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="first_reset",
            header_name="First Reset Date",
            filter=AGFilters.text,
            min_width=130,
        ),
        ag_grid.column_def(
            field="expiry",
            header_name="Expiry Date",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="latest_reset",
            header_name="Latest Reset Date",
            filter=AGFilters.text,
            min_width=130,
        ),
        ag_grid.column_def(
            field="reset_up_down",
            header_name="Reset Up/Down",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="market_price",
            header_name="Market Price",
            filter=AGFilters.text,
            min_width=110,
        ),
    ]


def reset_dates_ag_grid() -> rx.Component:
    return ag_grid(
        id="reset_dates_grid",
        row_data=PortfolioToolsState.filtered_reset_dates,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={"sortable": True, "resizable": True, "filter": True},
        height="calc(100vh - 300px)",
        width="100%",
    )
