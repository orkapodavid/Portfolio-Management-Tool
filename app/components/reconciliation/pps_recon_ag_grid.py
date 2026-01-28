"""
PPS Recon AG-Grid Component.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.reconciliation.reconciliation_state import ReconciliationState


def _get_column_defs() -> list:
    return [
        ag_grid.column_def(
            field="value_date",
            header_name="Value Date",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="trade_date",
            header_name="Trade Date",
            filter=AGFilters.text,
            min_width=100,
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
            field="code", header_name="Code", filter=AGFilters.text, min_width=80
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
            field="pos_loc", header_name="Pos Loc", filter=AGFilters.text, min_width=80
        ),
        ag_grid.column_def(
            field="account", header_name="Account", filter=AGFilters.text, min_width=100
        ),
    ]


def pps_recon_ag_grid() -> rx.Component:
    return ag_grid(
        id="pps_recon_grid",
        row_data=ReconciliationState.filtered_pps_recon,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={"sortable": True, "resizable": True, "filter": True},
        height="100%",
        width="100%",
    )
