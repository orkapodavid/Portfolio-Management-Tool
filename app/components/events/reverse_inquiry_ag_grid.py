"""
Reverse Inquiry AG-Grid Component.

AG-Grid based implementation for reverse inquiry table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.events.events_state import EventsState


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the reverse inquiry grid."""
    return [
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="company",
            header_name="Company",
            filter=AGFilters.text,
            min_width=150,
        ),
        ag_grid.column_def(
            field="inquiry_date",
            header_name="Inquiry Date",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="expiry_date",
            header_name="Expiry Date",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="deal_point",
            header_name="Deal Point",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="agent",
            header_name="Agent",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="notes",
            header_name="Notes",
            filter=AGFilters.text,
            min_width=150,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================


def reverse_inquiry_ag_grid() -> rx.Component:
    """
    Reverse Inquiry AG-Grid component.

    Displays reverse inquiry data.
    """
    return ag_grid(
        id="reverse_inquiry_grid",
        row_data=EventsState.filtered_reverse_inquiry,
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
