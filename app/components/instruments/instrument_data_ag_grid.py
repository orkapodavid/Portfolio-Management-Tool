"""Instrument Data AG-Grid Component."""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.instruments.instrument_state import InstrumentState


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
            field="sec_id", header_name="SecID", filter=AGFilters.text, min_width=90
        ),
        ag_grid.column_def(
            field="sec_type",
            header_name="Sec Type",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="pos_loc",
            header_name="Position Location",
            filter=AGFilters.text,
            min_width=130,
        ),
        ag_grid.column_def(
            field="account", header_name="Account", filter=AGFilters.text, min_width=100
        ),
    ]


def instrument_data_ag_grid() -> rx.Component:
    return ag_grid(
        id="instrument_data_grid",
        row_data=InstrumentState.filtered_instrument_data,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={"sortable": True, "resizable": True, "filter": True},
        height="100%",
        width="100%",
    )
