"""Special Term AG-Grid Component."""

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
            field="pos_loc",
            header_name="Position Location",
            filter=AGFilters.text,
            min_width=130,
        ),
        ag_grid.column_def(
            field="account", header_name="Account", filter=AGFilters.text, min_width=100
        ),
        ag_grid.column_def(
            field="effective_date",
            header_name="Effective Date",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="position",
            header_name="Position",
            filter=AGFilters.text,
            min_width=90,
        ),
    ]


def special_term_ag_grid() -> rx.Component:
    return ag_grid(
        id="special_term_grid",
        row_data=InstrumentState.filtered_special_terms,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={"sortable": True, "resizable": True, "filter": True},
        height="calc(100vh - 300px)",
        width="100%",
    )
