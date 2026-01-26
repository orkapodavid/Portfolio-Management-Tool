"""Deal Indication AG-Grid Component."""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.portfolio_tools.portfolio_tools_state import PortfolioToolsState


def _get_column_defs() -> list:
    return [
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
            field="identification",
            header_name="Identification",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="deal_type",
            header_name="Deal Type",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="agent", header_name="Agent", filter=AGFilters.text, min_width=100
        ),
        ag_grid.column_def(
            field="captain",
            header_name="Deal Captain",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="indication_date",
            header_name="Indication Date",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="currency",
            header_name="Currency",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="market_cap_loc",
            header_name="Market Cap LOC",
            filter=AGFilters.text,
            min_width=130,
        ),
        ag_grid.column_def(
            field="gross_proceed_loc",
            header_name="Gross Proceed LOC",
            filter=AGFilters.text,
            min_width=140,
        ),
        ag_grid.column_def(
            field="indication_amount",
            header_name="Indication Amount",
            filter=AGFilters.text,
            min_width=140,
        ),
    ]


def deal_indication_ag_grid() -> rx.Component:
    return ag_grid(
        id="deal_indication_grid",
        row_data=PortfolioToolsState.filtered_deal_indication,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={"sortable": True, "resizable": True, "filter": True},
        height="calc(100vh - 300px)",
        width="100%",
    )
