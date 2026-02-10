"""
Reverse Inquiry AG-Grid Component.

AG-Grid based implementation for reverse inquiry table, replacing legacy rx.el.table.
Migrated to use create_standard_grid factory with full toolbar support.
Includes a position date selector that triggers database reload.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.events.events_state import EventsState
from app.components.shared.ag_grid_config import (
    create_standard_grid,
    filter_date_input,
    FILTER_LABEL_CLASS,
    FILTER_INPUT_CLASS,
)


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class ReverseInquiryGridState(rx.State):
    """State for Reverse Inquiry grid quick filter."""

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
    """Return column definitions for the reverse inquiry grid."""
    return [
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
            field="inquiry_date",
            header_name="Inquiry Date",
            filter=AGFilters.date,
            min_width=100,
        ),
        ag_grid.column_def(
            field="expiry_date",
            header_name="Expiry Date",
            filter=AGFilters.date,
            min_width=100,
        ),
        ag_grid.column_def(
            field="deal_point",
            header_name="Deal Point",
            filter=AGFilters.text,
            min_width=100,
            tooltip_field="deal_point",
        ),
        ag_grid.column_def(
            field="agent",
            header_name="Agent",
            filter=AGFilters.text,
            min_width=100,
            tooltip_field="agent",
        ),
        ag_grid.column_def(
            field="notes",
            header_name="Notes",
            filter=AGFilters.text,
            min_width=150,
            tooltip_field="notes",
        ),
    ]


# =============================================================================
# POSITION DATE FILTER BAR
# =============================================================================


def _position_date_bar() -> rx.Component:
    """Position date selector bar — triggers data reload on change."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("calendar", size=14, class_name="text-gray-400"),
                rx.el.span(
                    "POSITION DATE",
                    class_name=FILTER_LABEL_CLASS,
                ),
                rx.el.input(
                    type="date",
                    value=EventsState.reverse_inquiry_position_date,
                    on_change=EventsState.set_reverse_inquiry_position_date,
                    class_name=f"{FILTER_INPUT_CLASS} w-[150px]",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        class_name=(
            "px-3 py-2 bg-gradient-to-r from-gray-50/80 to-slate-50/80 "
            "border border-gray-100 rounded-lg backdrop-blur-sm"
        ),
    )


# =============================================================================
# MAIN COMPONENT
# =============================================================================

# Storage key for grid state persistence
_STORAGE_KEY = "reverse_inquiry_grid_state"
_GRID_ID = "reverse_inquiry_grid"


def reverse_inquiry_ag_grid() -> rx.Component:
    """
    Reverse Inquiry AG-Grid component.

    Displays reverse inquiry data with full toolbar support:
    - Position date selector (defaults to today, auto-reloads on change)
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
            page_name="reverse_inquiry",
            search_value=ReverseInquiryGridState.search_text,
            on_search_change=ReverseInquiryGridState.set_search,
            on_search_clear=ReverseInquiryGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
            # Status Bar: Last Updated + Force Refresh
            last_updated=EventsState.reverse_inquiry_last_updated,
            show_refresh=True,
            on_refresh=EventsState.force_refresh_reverse_inquiry,
            is_loading=EventsState.is_loading_reverse_inquiry,
        ),
        # Position date selector bar
        _position_date_bar(),
        # Grid with factory pattern
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=EventsState.reverse_inquiry,
            column_defs=_get_column_defs(),
            row_id_key="id",  # Delta detection key (unique row ID)
            loading=EventsState.is_loading_reverse_inquiry,  # Loading overlay
            enable_row_numbers=True,  # Tier 2: Row numbering
            enable_multi_select=True,  # Tier 2: Multi-row selection with checkboxes
            default_excel_export_params=get_default_export_params("reverse_inquiry"),
            default_csv_export_params=get_default_csv_export_params("reverse_inquiry"),
            quick_filter_text=ReverseInquiryGridState.search_text,
        ),
        width="100%",
        height="100%",
        spacing="0",
        on_mount=EventsState.load_reverse_inquiry_data,
    )
