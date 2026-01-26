"""Instrument Term AG-Grid Component."""

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
            field="sec_type",
            header_name="Sec Type",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="effective_date",
            header_name="Effective Date",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="maturity_date",
            header_name="Maturity Date",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="first_reset_da",
            header_name="First Reset Da (truncated)",
            filter=AGFilters.text,
            min_width=160,
        ),
    ]


def instrument_term_ag_grid() -> rx.Component:
    return ag_grid(
        id="instrument_term_grid",
        row_data=InstrumentState.filtered_instrument_terms,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={"sortable": True, "resizable": True, "filter": True},
        height="calc(100vh - 300px)",
        width="100%",
    )
