"""
Event Calendar AG-Grid Component.

AG-Grid based implementation for event calendar table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.events.events_state import EventsState


# =============================================================================
# COLUMN DEFINITIONS
# =============================================================================


def _get_column_defs() -> list:
    """Return column definitions for the event calendar grid."""
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
            field="company",
            header_name="Company",
            filter=AGFilters.text,
            min_width=150,
        ),
        ag_grid.column_def(
            field="event_date",
            header_name="Event Date",
            filter=AGFilters.text,
            min_width=100,
        ),
        ag_grid.column_def(
            field="day_of_week",
            header_name="Day Of Week",
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
            field="time",
            header_name="Time",
            filter=AGFilters.text,
            min_width=80,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================


def event_calendar_ag_grid() -> rx.Component:
    """
    Event Calendar AG-Grid component.

    Displays event calendar data.
    """
    return ag_grid(
        id="event_calendar_grid",
        row_data=EventsState.filtered_event_calendar,
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
