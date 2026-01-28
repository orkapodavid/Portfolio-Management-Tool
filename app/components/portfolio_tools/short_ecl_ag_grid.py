"""Short ECL AG-Grid Component."""

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
            field="pos_loc", header_name="Pos Loc", filter=AGFilters.text, min_width=80
        ),
        ag_grid.column_def(
            field="account", header_name="Account", filter=AGFilters.text, min_width=100
        ),
        ag_grid.column_def(
            field="short_position",
            header_name="Short Position",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="nosh", header_name="NOSH", filter=AGFilters.text, min_width=80
        ),
        ag_grid.column_def(
            field="short_ownership",
            header_name="Short Ownership",
            filter=AGFilters.text,
            min_width=130,
        ),
        ag_grid.column_def(
            field="last_volume",
            header_name="Last Volume",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="short_pos_truncated",
            header_name="ShortPos/(truncated)",
            filter=AGFilters.text,
            min_width=150,
        ),
    ]


def short_ecl_ag_grid() -> rx.Component:
    return ag_grid(
        id="short_ecl_grid",
        row_data=PortfolioToolsState.filtered_short_ecl,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={"sortable": True, "resizable": True, "filter": True},
        height="100%",
        width="100%",
    )
