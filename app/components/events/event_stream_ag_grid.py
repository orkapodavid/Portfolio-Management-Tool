"""
Event Stream AG-Grid Component.

AG-Grid based implementation for event stream table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.events.events_state import EventsState


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the event stream grid."""
    return [
        ag_grid.column_def(
            field="symbol",
            header_name="Symbol",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="record_date",
            header_name="Record Date",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="event_date",
            header_name="Event Date",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="day_of_week",
            header_name="Day of Week",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="event_type",
            header_name="Event Type",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="subject",
            header_name="Subject",
            filter=AGFilters.text,
            min_width=150,
        ),
        ag_grid.column_def(
            field="notes",
            header_name="Notes",
            filter=AGFilters.text,
            min_width=150,
        ),
        ag_grid.column_def(
            field="alerted",
            header_name="Alerted?",
            filter=AGFilters.text,
            min_width=80,
        ),
        ag_grid.column_def(
            field="recur",
            header_name="Recur?",
            filter=AGFilters.text,
            min_width=80,
        ),
        ag_grid.column_def(
            field="created_by",
            header_name="Created By",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="created_time",
            header_name="Created Time",
            filter=AGFilters.text,
            min_width=110,
        ),
        ag_grid.column_def(
            field="updated_by",
            header_name="Updated By",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="updated_time",
            header_name="Updated Time",
            filter=AGFilters.text,
            min_width=110,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================


def event_stream_ag_grid() -> rx.Component:
    """
    Event Stream AG-Grid component.

    Displays event stream data.
    """
    return ag_grid(
        id="event_stream_grid",
        row_data=EventsState.filtered_event_stream,
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
