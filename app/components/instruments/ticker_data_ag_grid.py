"""Ticker Data AG-Grid Component."""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.instruments.instrument_state import InstrumentState


def _get_column_defs() -> list:
    return [
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
            field="fx_rate", header_name="FX Rate", filter=AGFilters.text, min_width=90
        ),
        ag_grid.column_def(
            field="sector", header_name="Sector", filter=AGFilters.text, min_width=100
        ),
        ag_grid.column_def(
            field="company", header_name="Company", filter=AGFilters.text, min_width=150
        ),
        ag_grid.column_def(
            field="po_lead_manager",
            header_name="PO Lead Manager",
            filter=AGFilters.text,
            min_width=130,
        ),
        ag_grid.column_def(
            field="fmat_cap",
            header_name="FMat Cap",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="smkt_cap",
            header_name="SMkt Cap",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="chg_1d_pct", header_name="1D%", filter=AGFilters.text, min_width=80
        ),
        ag_grid.column_def(
            field="dtl", header_name="DTL", filter=AGFilters.text, min_width=80
        ),
    ]


def ticker_data_ag_grid() -> rx.Component:
    return ag_grid(
        id="ticker_data_grid",
        row_data=InstrumentState.filtered_ticker_data,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={"sortable": True, "resizable": True, "filter": True},
        height="calc(100vh - 300px)",
        width="100%",
    )
