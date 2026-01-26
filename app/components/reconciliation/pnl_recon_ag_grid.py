"""
PnL Recon AG-Grid Component.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.reconciliation.reconciliation_state import ReconciliationState


def _get_column_defs() -> list:
    return [
        ag_grid.column_def(
            field="trade_date",
            header_name="Trade Date",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="report_date",
            header_name="Report Date",
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
            field="row_index",
            header_name="Row Index",
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
            field="pos_loc", header_name="Pos Loc", filter=AGFilters.text, min_width=80
        ),
        ag_grid.column_def(
            field="stock_sec_id",
            header_name="Stock SecID",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="warrant_sec_id",
            header_name="Warrant SecID",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="bond_sec_id",
            header_name="Bond SecID",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="stock_position",
            header_name="Stock Position",
            filter=AGFilters.text,
            min_width=110,
        ),
    ]


def pnl_recon_ag_grid() -> rx.Component:
    return ag_grid(
        id="pnl_recon_grid",
        row_data=ReconciliationState.filtered_pnl_recon,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={"sortable": True, "resizable": True, "filter": True},
        height="calc(100vh - 300px)",
        width="100%",
    )
