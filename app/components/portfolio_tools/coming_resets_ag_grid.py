"""Coming Resets AG-Grid Component."""

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
            field="detail_id",
            header_name="Detail ID",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="ticker", header_name="Ticker", filter=AGFilters.text, min_width=100
        ),
        ag_grid.column_def(
            field="account", header_name="Account", filter=AGFilters.text, min_width=100
        ),
        ag_grid.column_def(
            field="company_name",
            header_name="Company Name",
            filter=AGFilters.text,
            min_width=150,
        ),
        ag_grid.column_def(
            field="announce_date",
            header_name="Announcement Date",
            filter=AGFilters.text,
            min_width=140,
        ),
        ag_grid.column_def(
            field="closing_date",
            header_name="Closing Date",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="cal_days",
            header_name="Cal Days Since Announced",
            filter=AGFilters.text,
            min_width=180,
        ),
        ag_grid.column_def(
            field="biz_days",
            header_name="Biz Days Since Announced",
            filter=AGFilters.text,
            min_width=180,
        ),
    ]


def coming_resets_ag_grid() -> rx.Component:
    return ag_grid(
        id="coming_resets_grid",
        row_data=PortfolioToolsState.filtered_coming_resets,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={"sortable": True, "resizable": True, "filter": True},
        height="calc(100vh - 300px)",
        width="100%",
    )
