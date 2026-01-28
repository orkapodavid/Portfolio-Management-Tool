"""
Monthly Exercise Limit AG-Grid Component.

AG-Grid based implementation for monthly exercise limit table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.compliance.compliance_state import ComplianceState


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the monthly exercise limit grid."""
    return [
        ag_grid.column_def(
            field="underlying",
            header_name="Underlying",
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
            field="sec_type",
            header_name="Sec Type",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="original_nosh",
            header_name="Original Nosh",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="original_quantity",
            header_name="Original Quantity",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="monthly_exercised_quantity",
            header_name="Monthly Exercised Qty",
            filter=AGFilters.text,
            min_width=150,
        ),
        ag_grid.column_def(
            field="monthly_exercised_pct",
            header_name="Monthly Exercised %",
            filter=AGFilters.text,
            min_width=130,
        ),
        ag_grid.column_def(
            field="monthly_sal",
            header_name="Monthly Sal",
            filter=AGFilters.text,
            min_width=100,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================


def monthly_exercise_limit_ag_grid() -> rx.Component:
    """
    Monthly Exercise Limit AG-Grid component.

    Displays monthly exercise limit compliance data.
    """
    return ag_grid(
        id="monthly_exercise_limit_grid",
        row_data=ComplianceState.filtered_monthly_exercise_limit,
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
