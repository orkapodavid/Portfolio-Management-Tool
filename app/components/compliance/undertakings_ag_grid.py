"""
Undertakings AG-Grid Component.

AG-Grid based implementation for undertakings table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.compliance.compliance_state import ComplianceState
from app.components.shared.ag_grid_config import (
    create_standard_grid,
    FILTER_LABEL_CLASS,
    FILTER_INPUT_CLASS,
)


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class UndertakingsGridState(rx.State):
    """State for Undertakings grid quick filter."""

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
    """Return column definitions for the undertakings grid."""
    return [
        ag_grid.column_def(
            field="deal_num",
            header_name="Deal Num",
            filter=AGFilters.text,
            min_width=90,
            tooltip_field="deal_num",
        ),
        ag_grid.column_def(
            field="ticker",
            header_name="Ticker",
            filter=AGFilters.text,
            min_width=100,
            enable_row_group=True,
            tooltip_field="ticker",
            pinned="left",  # Keep visible while scrolling
        ),
        ag_grid.column_def(
            field="company_name",
            header_name="Company Name",
            filter=AGFilters.text,
            min_width=150,
            tooltip_field="company_name",  # Show full name on hover
        ),
        ag_grid.column_def(
            field="account",
            header_name="Account",
            filter=AGFilters.text,
            min_width=100,
            enable_row_group=True,
            tooltip_field="account",
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
            filter="agSetColumnFilter",  # Tier 2: Set filter for categorical
            min_width=120,
            enable_row_group=True,
        ),
        ag_grid.column_def(
            field="undertaking_details",
            header_name="Undertaking Details",
            filter=AGFilters.text,
            min_width=150,
            tooltip_field="undertaking_details",  # Full details on hover
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

# Storage key for grid state persistence
_STORAGE_KEY = "undertakings_grid_state"


# =============================================================================
# POSITION DATE FILTER BAR
# =============================================================================


def _position_date_bar() -> rx.Component:
    """Position date selector bar."""
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("calendar", size=14, class_name="text-gray-400"),
                rx.el.span("POSITION DATE", class_name=FILTER_LABEL_CLASS),
                rx.el.input(
                    type="date",
                    value=ComplianceState.undertakings_position_date,
                    on_change=ComplianceState.set_undertakings_position_date,
                    class_name=f"{FILTER_INPUT_CLASS} w-[150px]",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex items-center justify-between w-full",
        ),
        class_name=(
            "w-full px-3 py-2 bg-gradient-to-r from-gray-50/80 to-slate-50/80 "
            "border-b border-gray-100 backdrop-blur-sm"
        ),
    )


def undertakings_ag_grid() -> rx.Component:
    """
    Undertakings AG-Grid component.

    Displays undertakings compliance data with Tier 1 enhancements:
    - Quick filter search across all columns
    - Excel export button
    - Full grid state persistence (columns + filters + sort)
    - Status bar with row counts
    - Range selection
    - Floating filters
    - No-rows overlay
    """
    from app.components.shared.ag_grid_config import (
        grid_state_script,
        grid_toolbar,
        get_default_export_params,
        get_default_csv_export_params,
    )

    return rx.vstack(
        # Grid state persistence script (auto-restores on page load)
        rx.script(grid_state_script(_STORAGE_KEY, "undertakings_grid")),
        # Toolbar with grouped buttons (Export | Layout)
        grid_toolbar(
            storage_key=_STORAGE_KEY,
            page_name="undertakings",
            search_value=UndertakingsGridState.search_text,
            on_search_change=UndertakingsGridState.set_search,
            on_search_clear=UndertakingsGridState.clear_search,
            grid_id="undertakings_grid",
            show_compact_toggle=True,
            # Status Bar: Last Updated + Force Refresh
            last_updated=ComplianceState.undertakings_last_updated,
            show_refresh=True,
            on_refresh=ComplianceState.force_refresh_undertakings,
            is_loading=ComplianceState.is_loading_undertakings,
        ),
        _position_date_bar(),
        # Grid with row grouping support
        create_standard_grid(
            grid_id="undertakings_grid",
            row_data=ComplianceState.filtered_undertakings,
            column_defs=_get_column_defs(),
            row_id_key="id",  # Delta detection key (unique row ID)
            loading=ComplianceState.is_loading_undertakings,  # Loading overlay
            enable_row_numbers=True,  # Tier 2: Row numbering
            enable_multi_select=True,  # Tier 2: Multi-row selection with checkboxes
            default_excel_export_params=get_default_export_params("undertakings"),
            default_csv_export_params=get_default_csv_export_params("undertakings"),
            quick_filter_text=UndertakingsGridState.search_text,
            # Row grouping options
            row_group_panel_show="always",
            group_default_expanded=-1,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
