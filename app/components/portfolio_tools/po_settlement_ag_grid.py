"""PO Settlement AG-Grid Component."""

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
            field="ticker", header_name="Ticker", filter=AGFilters.text, min_width=100
        ),
        ag_grid.column_def(
            field="company_name",
            header_name="Company Name",
            filter=AGFilters.text,
            min_width=150,
        ),
        ag_grid.column_def(
            field="structure",
            header_name="Structure",
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
            field="fx_rate", header_name="FX Rate", filter=AGFilters.text, min_width=90
        ),
        ag_grid.column_def(
            field="last_price",
            header_name="Last Price",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="current_position",
            header_name="Current Position",
            filter=AGFilters.text,
            min_width=130,
        ),
        ag_grid.column_def(
            field="shares_allocated",
            header_name="Shares Allocated",
            filter=AGFilters.text,
            min_width=130,
        ),
        ag_grid.column_def(
            field="shares_swap",
            header_name="Shares in Swap",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="shares_hedged",
            header_name="Shares Hedged",
            filter=AGFilters.text,
            min_width=120,
        ),
    ]


def po_settlement_ag_grid() -> rx.Component:
    return ag_grid(
        id="po_settlement_grid",
        row_data=PortfolioToolsState.filtered_po_settlement,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={"sortable": True, "resizable": True, "filter": True},
        height="calc(100vh - 300px)",
        width="100%",
    )
