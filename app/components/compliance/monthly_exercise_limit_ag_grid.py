"""
Monthly Exercise Limit AG-Grid Component.

AG-Grid based implementation for monthly exercise limit table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.compliance.compliance_state import ComplianceState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class MonthlyExerciseLimitGridState(rx.State):
    """State for Monthly Exercise Limit grid quick filter."""

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
    """Return column definitions for the monthly exercise limit grid."""
    return [
        ag_grid.column_def(
            field="underlying",
            header_name="Underlying",
            filter=AGFilters.text,
            min_width=100,
            enable_row_group=True,
            tooltip_field="underlying",
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
            tooltip_field="company_name",
        ),
        ag_grid.column_def(
            field="sec_type",
            header_name="Sec Type",
            filter="agSetColumnFilter",  # Tier 2: Set filter for categorical
            min_width=90,
            enable_row_group=True,
        ),
        ag_grid.column_def(
            field="original_nosh",
            header_name="Original Nosh",
            filter=AGFilters.number,
            min_width=110,
        ),
        ag_grid.column_def(
            field="original_quantity",
            header_name="Original Quantity",
            filter=AGFilters.number,
            min_width=120,
            agg_func="sum",
        ),
        ag_grid.column_def(
            field="monthly_exercised_quantity",
            header_name="Monthly Exercised Qty",
            filter=AGFilters.number,
            min_width=150,
            agg_func="sum",
        ),
        ag_grid.column_def(
            field="monthly_exercised_pct",
            header_name="Monthly Exercised %",
            filter=AGFilters.number,
            min_width=130,
            agg_func="avg",  # Use avg for percentages
        ),
        ag_grid.column_def(
            field="monthly_sal",
            header_name="Monthly Sal",
            filter=AGFilters.number,
            min_width=100,
            agg_func="sum",
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

# Storage key and grid ID for state persistence
_STORAGE_KEY = "monthly_exercise_limit_grid_state"
_GRID_ID = "monthly_exercise_limit_grid"


def monthly_exercise_limit_ag_grid() -> rx.Component:
    """
    Monthly Exercise Limit AG-Grid component.

    Displays monthly exercise limit compliance data with Tier 1 enhancements:
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
            page_name="monthly_exercise_limit",
            search_value=MonthlyExerciseLimitGridState.search_text,
            on_search_change=MonthlyExerciseLimitGridState.set_search,
            on_search_clear=MonthlyExerciseLimitGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
        ),
        # Grid with row grouping support
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=ComplianceState.filtered_monthly_exercise_limit,
            column_defs=_get_column_defs(),
            enable_row_numbers=True,  # Tier 2: Row numbering
            enable_multi_select=True,  # Tier 2: Multi-row selection with checkboxes
            default_excel_export_params=get_default_export_params("monthly_exercise_limit"),
            default_csv_export_params=get_default_csv_export_params("monthly_exercise_limit"),
            quick_filter_text=MonthlyExerciseLimitGridState.search_text,
            # Row grouping options
            row_group_panel_show="always",
            group_default_expanded=-1,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
