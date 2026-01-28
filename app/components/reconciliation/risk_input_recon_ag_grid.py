"""
Risk Input Recon AG-Grid Component.
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
            field="underlying",
            header_name="Underlying",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="ticker", header_name="Ticker", filter=AGFilters.text, min_width=100
        ),
        ag_grid.column_def(
            field="sec_type",
            header_name="Sec Type",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="spot_mc",
            header_name="Spot (MC)",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="spot_ppd",
            header_name="Spot (PPD)",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="position",
            header_name="Position",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="value_mc",
            header_name="Value (MC)",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="value_ppd",
            header_name="Value (PPD)",
            filter=AGFilters.text,
            min_width=90,
        ),
    ]


def risk_input_recon_ag_grid() -> rx.Component:
    return ag_grid(
        id="risk_input_recon_grid",
        row_data=ReconciliationState.filtered_risk_input_recon,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={"sortable": True, "resizable": True, "filter": True},
        height="100%",
        width="100%",
    )
