"""Stock Screener AG-Grid Component."""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.instruments.instrument_state import InstrumentState


def _get_column_defs() -> list:
    return [
        ag_grid.column_def(
            field="otl", header_name="OTL", filter=AGFilters.text, min_width=70
        ),
        ag_grid.column_def(
            field="mkt_cap_37_pct",
            header_name="37% Market Cap",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="ticker", header_name="Ticker", filter=AGFilters.text, min_width=100
        ),
        ag_grid.column_def(
            field="company", header_name="Company", filter=AGFilters.text, min_width=150
        ),
        ag_grid.column_def(
            field="country", header_name="Country", filter=AGFilters.text, min_width=90
        ),
        ag_grid.column_def(
            field="industry",
            header_name="Industry",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="last_price",
            header_name="Last Price",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="mkt_cap_loc",
            header_name="Market Cap (MM LOC)",
            filter=AGFilters.text,
            min_width=150,
        ),
        ag_grid.column_def(
            field="mkt_cap_usd",
            header_name="Market Cap (MM USD)",
            filter=AGFilters.text,
            min_width=150,
        ),
        ag_grid.column_def(
            field="adv_3m", header_name="ADV 3M", filter=AGFilters.text, min_width=90
        ),
        ag_grid.column_def(
            field="locate_qty_mm",
            header_name="Locate Qty (MM)",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="locate_f",
            header_name="Locate F",
            filter=AGFilters.text,
            min_width=90,
        ),
    ]


def stock_screener_ag_grid() -> rx.Component:
    return ag_grid(
        id="stock_screener_grid",
        row_data=InstrumentState.filtered_stock_screener,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={"sortable": True, "resizable": True, "filter": True},
        height="100%",
        width="100%",
    )
