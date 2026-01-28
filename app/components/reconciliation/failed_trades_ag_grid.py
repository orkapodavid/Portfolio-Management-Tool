"""
Failed Trades AG-Grid Component.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.reconciliation.reconciliation_state import ReconciliationState


def _get_column_defs() -> list:
    return [
        ag_grid.column_def(
            field="report_date",
            header_name="Report Date",
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
            field="value_date",
            header_name="Value Date",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="settlement_date",
            header_name="Settlement Date",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="portfolio_code",
            header_name="Portfolio Code",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="instrument_ref",
            header_name="Instrument Ref",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="instrument_name",
            header_name="Instrument Name",
            filter=AGFilters.text,
            min_width=130,
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
            field="isin", header_name="ISIN", filter=AGFilters.text, min_width=110
        ),
        ag_grid.column_def(
            field="sedol", header_name="SEDOL", filter=AGFilters.text, min_width=90
        ),
        ag_grid.column_def(
            field="broker", header_name="Broker", filter=AGFilters.text, min_width=100
        ),
        ag_grid.column_def(
            field="glass_reference",
            header_name="Glass Reference",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="trade_reference",
            header_name="Trade Reference",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="deal_type",
            header_name="Deal Type",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="q", header_name="Q", filter=AGFilters.text, min_width=60
        ),
    ]


def failed_trades_ag_grid() -> rx.Component:
    return ag_grid(
        id="failed_trades_grid",
        row_data=ReconciliationState.filtered_failed_trades,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={"sortable": True, "resizable": True, "filter": True},
        height="100%",
        width="100%",
    )
