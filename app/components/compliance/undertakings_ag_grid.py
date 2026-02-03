"""
Undertakings AG-Grid Component.

AG-Grid based implementation for undertakings table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.compliance.compliance_state import ComplianceState
from app.components.shared.ag_grid_config import create_standard_grid


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
        ),
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
            field="account",
            header_name="Account",
            filter=AGFilters.text,
            min_width=100,
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
        ),
        ag_grid.column_def(
            field="undertaking_details",
            header_name="Undertaking Details",
            filter=AGFilters.text,
            min_width=150,
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

# Storage key for column state persistence
_STORAGE_KEY = "undertakings_column_state"


def undertakings_ag_grid() -> rx.Component:
    """
    Undertakings AG-Grid component.

    Displays undertakings compliance data with Tier 1 enhancements:
    - Quick filter search across all columns
    - Excel export button
    - Column state persistence (auto-save + restore/reset)
    - Status bar with row counts
    - Range selection
    - Floating filters
    - No-rows overlay
    """
    from app.components.shared.ag_grid_config import (
        export_button,
        column_state_buttons,
        quick_filter_input,
        get_default_export_params,
        get_default_csv_export_params,
    )

    return rx.vstack(
        # Toolbar
        rx.hstack(
            # Left side: Quick filter
            quick_filter_input(
                search_value=UndertakingsGridState.search_text,
                on_change=UndertakingsGridState.set_search,
                on_clear=UndertakingsGridState.clear_search,
            ),
            # Right side: Export and column buttons
            rx.hstack(
                export_button(page_name="undertakings"),
                column_state_buttons(
                    _STORAGE_KEY, show_save=True
                ),  # Manual save since auto-save not supported
                gap="4",
            ),
            justify="between",
            width="100%",
            padding_bottom="2",
        ),
        # Grid
        create_standard_grid(
            grid_id="undertakings_grid",
            row_data=ComplianceState.filtered_undertakings,
            column_defs=_get_column_defs(),
            enable_row_numbers=True,  # Tier 2: Row numbering
            enable_multi_select=True,  # Tier 2: Multi-row selection with checkboxes
            default_excel_export_params=get_default_export_params("undertakings"),
            default_csv_export_params=get_default_csv_export_params("undertakings"),
            quick_filter_text=UndertakingsGridState.search_text,  # Quick filter
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
