"""
Event Calendar AG-Grid Component.

AG-Grid based implementation for event calendar table, replacing legacy rx.el.table.
Migrated to use create_standard_grid factory with full toolbar support.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.events.events_state import EventsState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class EventCalendarGridState(rx.State):
    """State for Event Calendar grid quick filter."""

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
    """Return column definitions for the event calendar grid."""
    return [
        ag_grid.column_def(
            field="underlying",
            header_name="Underlying",
            filter=AGFilters.text,
            min_width=100,
            tooltip_field="underlying",
        ),
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
            tooltip_field="ticker",
            pinned="left",  # Keep ticker visible while scrolling
        ),
        ag_grid.column_def(
            field="company",
            header_name="Company",
            filter=AGFilters.text,
            min_width=150,
            tooltip_field="company",
        ),
        ag_grid.column_def(
            field="event_date",
            header_name="Event Date",
            filter=AGFilters.date,
            min_width=100,
        ),
        ag_grid.column_def(
            field="day_of_week",
            header_name="Day Of Week",
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
            field="time",
            header_name="Time",
            filter=AGFilters.text,
            min_width=80,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

# Storage key for grid state persistence
_STORAGE_KEY = "event_calendar_grid_state"
_GRID_ID = "event_calendar_grid"


def event_calendar_ag_grid() -> rx.Component:
    """
    Event Calendar AG-Grid component.

    Displays event calendar data with full toolbar support:
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
            page_name="event_calendar",
            search_value=EventCalendarGridState.search_text,
            on_search_change=EventCalendarGridState.set_search,
            on_search_clear=EventCalendarGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            # Status Bar: Last Updated + Force Refresh
            last_updated=EventsState.event_calendar_last_updated,
            show_refresh=True,
            on_refresh=EventsState.force_refresh_event_calendar,
            is_loading=EventsState.is_loading_event_calendar,
        ),
        # Grid with factory pattern
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=EventsState.event_calendar,
            column_defs=_get_column_defs(),
            row_id_key="id",  # Delta detection key (unique row ID)
            loading=EventsState.is_loading_event_calendar,  # Loading overlay
            enable_row_numbers=True,  # Tier 2: Row numbering
            enable_multi_select=True,  # Tier 2: Multi-row selection with checkboxes
            default_excel_export_params=get_default_export_params("event_calendar"),
            default_csv_export_params=get_default_csv_export_params("event_calendar"),
            quick_filter_text=EventCalendarGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
