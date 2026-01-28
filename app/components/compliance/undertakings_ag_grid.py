"""
Undertakings AG-Grid Component.

AG-Grid based implementation for undertakings table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.compliance.compliance_state import ComplianceState


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the undertakings grid."""
    return [
        ag_grid.column_def(
            field="deal_num",
            header_name="Deal Num",
            filter=AGFilters.text,
            min_width=90,
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
            field="account",
            header_name="Account",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="undertaking_expiry",
            header_name="Undertaking Expiry",
            filter=AGFilters.text,
            min_width=130,
        ),
        ag_grid.column_def(
            field="undertaking_type",
            header_name="Undertaking Type",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="undertaking_details",
            header_name="Undertaking Details",
            filter=AGFilters.text,
            min_width=150,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================


def undertakings_ag_grid() -> rx.Component:
    """
    Undertakings AG-Grid component.

    Displays undertakings compliance data.
    """
    return ag_grid(
        id="undertakings_grid",
        row_data=ComplianceState.filtered_undertakings,
        column_defs=_get_column_defs(),
        row_id_key="id",
        theme="quartz",
        default_col_def={
            "sortable": True,
            "resizable": True,
            "filter": True,
        },
        height="100%",
        width="100%",
    )
