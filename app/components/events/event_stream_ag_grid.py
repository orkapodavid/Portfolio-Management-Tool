"""
Event Stream AG-Grid Component.

AG-Grid based implementation for event stream table, replacing legacy rx.el.table.
Migrated to use create_standard_grid factory with full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.events.events_state import EventsState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class EventStreamGridState(rx.State):
    """State for Event Stream grid quick filter."""

    search_text: str = ""

    def set_search(self, value: str):
        """Update search text."""
        self.search_text = value

    def clear_search(self):
        """Clear search text."""
        self.search_text = ""


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
            tooltip_field="symbol",
            pinned="left",  # Keep symbol visible while scrolling
        ),
        ag_grid.column_def(
            field="record_date",
            header_name="Record Date",
            filter=AGFilters.date,
            min_width=100,
        ),
        ag_grid.column_def(
            field="event_date",
            header_name="Event Date",
            filter=AGFilters.date,
            min_width=100,
        ),
        ag_grid.column_def(
            field="day_of_week",
            header_name="Day of Week",
            filter="agSetColumnFilter",  # Categorical column
            min_width=100,
        ),
        ag_grid.column_def(
            field="event_type",
            header_name="Event Type",
            filter="agSetColumnFilter",  # Categorical column
            min_width=100,
        ),
        ag_grid.column_def(
            field="subject",
            header_name="Subject",
            filter=AGFilters.text,
            min_width=150,
            tooltip_field="subject",
        ),
        ag_grid.column_def(
            field="notes",
            header_name="Notes",
            filter=AGFilters.text,
            min_width=150,
            tooltip_field="notes",
        ),
        ag_grid.column_def(
            field="alerted",
            header_name="Alerted?",
            filter="agSetColumnFilter",  # Categorical (Yes/No)
            min_width=80,
        ),
        ag_grid.column_def(
            field="recur",
            header_name="Recur?",
            filter="agSetColumnFilter",  # Categorical (Yes/No)
            min_width=80,
        ),
        ag_grid.column_def(
            field="created_by",
            header_name="Created By",
            filter=AGFilters.text,
            min_width=100,
            tooltip_field="created_by",
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
            tooltip_field="updated_by",
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

# Storage key for grid state persistence
_STORAGE_KEY = "event_stream_grid_state"
_GRID_ID = "event_stream_grid"


def event_stream_ag_grid() -> rx.Component:
    """
    Event Stream AG-Grid component.

    Displays event stream data with full toolbar support:
    - Quick filter search across all columns
    - Excel export button
    - Full grid state persistence (columns + filters + sort)
    - Status bar with row counts
    - Compact mode toggle
    """
    from app.components.shared.ag_grid_config import (
        grid_state_script,
        grid_toolbar,
        get_default_export_params,
        get_default_csv_export_params,
    )

    return rx.vstack(
        # Grid state persistence script (auto-restores on page load)
        rx.script(grid_state_script(_STORAGE_KEY, _GRID_ID)),
        # Toolbar with grouped buttons (Export | Layout)
        grid_toolbar(
            storage_key=_STORAGE_KEY,
            page_name="event_stream",
            search_value=EventStreamGridState.search_text,
            on_search_change=EventStreamGridState.set_search,
            on_search_clear=EventStreamGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
        ),
        # Grid with factory pattern
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=EventsState.filtered_event_stream,
            column_defs=_get_column_defs(),
            enable_row_numbers=True,  # Tier 2: Row numbering
            enable_multi_select=True,  # Tier 2: Multi-row selection with checkboxes
            default_excel_export_params=get_default_export_params("event_stream"),
            default_csv_export_params=get_default_csv_export_params("event_stream"),
            quick_filter_text=EventStreamGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
