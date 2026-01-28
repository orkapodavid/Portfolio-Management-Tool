"""Pay To Hold AG-Grid Component."""

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
            field="currency",
            header_name="Currency",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="counter_party",
            header_name="Counter Party",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="side", header_name="Side", filter=AGFilters.text, min_width=70
        ),
        ag_grid.column_def(
            field="sl_rate", header_name="SL Rate", filter=AGFilters.text, min_width=80
        ),
        ag_grid.column_def(
            field="pth_amount_sod",
            header_name="PTH Amount SOD",
            filter=AGFilters.text,
            min_width=130,
        ),
        ag_grid.column_def(
            field="pth_amount",
            header_name="PTH Amount",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="emsa_order",
            header_name="EMSA ORDER AMOUNT",
            filter=AGFilters.text,
            min_width=150,
        ),
        ag_grid.column_def(
            field="emsa_remark",
            header_name="EMSA Order Remark",
            filter=AGFilters.text,
            min_width=140,
        ),
        ag_grid.column_def(
            field="emsa_working",
            header_name="EMSA Working",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="emsa_order_col",
            header_name="EMSA ORDER CONFIRMED",
            filter=AGFilters.text,
            min_width=160,
        ),
        ag_grid.column_def(
            field="emsa_filled",
            header_name="EMSA ORDER FILLED",
            filter=AGFilters.text,
            min_width=150,
        ),
    ]


def pay_to_hold_ag_grid() -> rx.Component:
    return ag_grid(
        id="pay_to_hold_grid",
        row_data=PortfolioToolsState.filtered_pay_to_hold,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={"sortable": True, "resizable": True, "filter": True},
        height="100%",
        width="100%",
    )
