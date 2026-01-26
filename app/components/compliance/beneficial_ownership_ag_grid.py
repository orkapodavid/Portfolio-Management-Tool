"""
Beneficial Ownership AG-Grid Component.

AG-Grid based implementation for beneficial ownership table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.compliance.compliance_state import ComplianceState


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the beneficial ownership grid."""
    return [
        ag_grid.column_def(
            field="trade_date",
            header_name="Trade Date",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="company_name",
            header_name="Company Name",
            filter=AGFilters.text,
            min_width=150,
        ),
        ag_grid.column_def(
            field="nosh_reported",
            header_name="NOSH (Reported)",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="nosh_bbg",
            header_name="NOSH (BBG)",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="nosh_proforma",
            header_name="NOSH Proforma",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="stock_shares",
            header_name="Stock Shares",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="warrant_shares",
            header_name="Warrant Shares",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="bond_shares",
            header_name="Bond Shares",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="total_shares",
            header_name="Total Shares",
            filter=AGFilters.text,
            min_width=100,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================


def beneficial_ownership_ag_grid() -> rx.Component:
    """
    Beneficial Ownership AG-Grid component.

    Displays beneficial ownership compliance data.
    """
    return ag_grid(
        id="beneficial_ownership_grid",
        row_data=ComplianceState.filtered_beneficial_ownership,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={
            "sortable": True,
            "resizable": True,
            "filter": True,
        },
        height="calc(100vh - 300px)",
        width="100%",
    )
