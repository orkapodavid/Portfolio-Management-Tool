"""
Restricted List AG-Grid Component.

AG-Grid based implementation for restricted list table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.compliance.compliance_state import ComplianceState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class RestrictedListGridState(rx.State):
    """State for Restricted List grid quick filter."""

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
    """Return column definitions for the restricted list grid."""
    return [
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
            tooltip_field="company_name",
        ),
        ag_grid.column_def(
            field="in_emdx",
            header_name="In EMDX?",
            filter="agSetColumnFilter",  # Tier 2: Set filter for boolean-like
            min_width=80,
        ),
        ag_grid.column_def(
            field="compliance_type",
            header_name="Compliance Type",
            filter="agSetColumnFilter",  # Tier 2: Set filter for categorical
            min_width=120,
            enable_row_group=True,
        ),
        ag_grid.column_def(
            field="firm_block",
            header_name="Firm Block",
            filter="agSetColumnFilter",  # Tier 2: Set filter for categorical
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

# Storage key and grid ID for state persistence
_STORAGE_KEY = "restricted_list_grid_state"
_GRID_ID = "restricted_list_grid"


def restricted_list_ag_grid() -> rx.Component:
    """
    Restricted List AG-Grid component.

    Displays restricted list compliance data with Tier 1 enhancements:
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
        rx.script(grid_state_script(_STORAGE_KEY, _GRID_ID)),
        # Toolbar with grouped buttons (Export | Layout)
        grid_toolbar(
            storage_key=_STORAGE_KEY,
            page_name="restricted_list",
            search_value=RestrictedListGridState.search_text,
            on_search_change=RestrictedListGridState.set_search,
            on_search_clear=RestrictedListGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
        ),
        # Grid with row grouping support
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=ComplianceState.filtered_restricted_list,
            column_defs=_get_column_defs(),
            enable_row_numbers=True,  # Tier 2: Row numbering
            enable_multi_select=True,  # Tier 2: Multi-row selection with checkboxes
            default_excel_export_params=get_default_export_params("restricted_list"),
            default_csv_export_params=get_default_csv_export_params("restricted_list"),
            quick_filter_text=RestrictedListGridState.search_text,
            # Row grouping options
            row_group_panel_show="always",
            group_default_expanded=-1,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
