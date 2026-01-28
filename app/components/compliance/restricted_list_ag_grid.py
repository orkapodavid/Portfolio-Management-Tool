"""
Restricted List AG-Grid Component.

AG-Grid based implementation for restricted list table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.compliance.compliance_state import ComplianceState


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the restricted list grid."""
    return [
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
            field="in_emdx",
            header_name="In EMDX?",
            filter=AGFilters.text,
            min_width=80,
        ),
        ag_grid.column_def(
            field="compliance_type",
            header_name="Compliance Type",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="firm_block",
            header_name="Firm_Block",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="compliance_start",
            header_name="Compliance Start",
            filter=AGFilters.text,
            min_width=120,
        ),
        ag_grid.column_def(
            field="nda_end",
            header_name="NDA End",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="mnpi_end",
            header_name="MNPI End",
            filter=AGFilters.text,
            min_width=90,
        ),
        ag_grid.column_def(
            field="wc_end",
            header_name="WC End",
            filter=AGFilters.text,
            min_width=90,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================


def restricted_list_ag_grid() -> rx.Component:
    """
    Restricted List AG-Grid component.

    Displays restricted list compliance data.
    """
    return ag_grid(
        id="restricted_list_grid",
        row_data=ComplianceState.filtered_restricted_list,
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
