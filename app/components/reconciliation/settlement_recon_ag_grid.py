"""
Settlement Recon AG-Grid Component.
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
            field="ml_report_date",
            header_name="ML Report Date",
            filter=AGFilters.text,
            min_width=110,
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
            field="company_name",
            header_name="Company Name",
            filter=AGFilters.text,
            min_width=150,
        ),
        ag_grid.column_def(
            field="pos_loc", header_name="Pos Loc", filter=AGFilters.text, min_width=80
        ),
        ag_grid.column_def(
            field="currency",
            header_name="Currency",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="sec_type",
            header_name="Sec Type",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="position_settled",
            header_name="Position Settled",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="ml_inventory",
            header_name="ML Inventory",
            filter=AGFilters.text,
            min_width=110,
        ),
    ]


def settlement_recon_ag_grid() -> rx.Component:
    return ag_grid(
        id="settlement_recon_grid",
        row_data=ReconciliationState.filtered_settlement_recon,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={"sortable": True, "resizable": True, "filter": True},
        height="calc(100vh - 300px)",
        width="100%",
    )
