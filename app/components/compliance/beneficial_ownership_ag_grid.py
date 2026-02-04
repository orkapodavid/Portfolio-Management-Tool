"""
Beneficial Ownership AG-Grid Component.

AG-Grid based implementation for beneficial ownership table, replacing legacy rx.el.table.
"""

import reflex as rx
from reflex_ag_grid import ag_grid, AGFilters
from app.states.compliance.compliance_state import ComplianceState
from app.components.shared.ag_grid_config import create_standard_grid


# =============================================================================
# QUICK FILTER STATE
# =============================================================================


class BeneficialOwnershipGridState(rx.State):
    """State for Beneficial Ownership grid quick filter."""

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
    """Return column definitions for the beneficial ownership grid."""
    return [
        ag_grid.column_def(
            field="trade_date",
            header_name="Trade Date",
            filter=AGFilters.text,
            min_width=100,
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
            field="nosh_reported",
            header_name="NOSH (Reported)",
            filter=AGFilters.number,
            min_width=120,
        ),
        ag_grid.column_def(
            field="nosh_bbg",
            header_name="NOSH (BBG)",
            filter=AGFilters.number,
            min_width=100,
        ),
        ag_grid.column_def(
            field="nosh_proforma",
            header_name="NOSH Proforma",
            filter=AGFilters.number,
            min_width=120,
        ),
        ag_grid.column_def(
            field="stock_shares",
            header_name="Stock Shares",
            filter=AGFilters.number,
            min_width=100,
            agg_func="sum",
        ),
        ag_grid.column_def(
            field="warrant_shares",
            header_name="Warrant Shares",
            filter=AGFilters.number,
            min_width=110,
            agg_func="sum",
        ),
        ag_grid.column_def(
            field="bond_shares",
            header_name="Bond Shares",
            filter=AGFilters.number,
            min_width=100,
            agg_func="sum",
        ),
        ag_grid.column_def(
            field="total_shares",
            header_name="Total Shares",
            filter=AGFilters.number,
            min_width=100,
            agg_func="sum",
        ),
    ]


# =============================================================================
# MAIN COMPONENT
# =============================================================================

# Storage key and grid ID for state persistence
_STORAGE_KEY = "beneficial_ownership_grid_state"
_GRID_ID = "beneficial_ownership_grid"


def beneficial_ownership_ag_grid() -> rx.Component:
    """
    Beneficial Ownership AG-Grid component.

    Displays beneficial ownership compliance data with Tier 1 enhancements:
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
            page_name="beneficial_ownership",
            search_value=BeneficialOwnershipGridState.search_text,
            on_search_change=BeneficialOwnershipGridState.set_search,
            on_search_clear=BeneficialOwnershipGridState.clear_search,
            grid_id=_GRID_ID,
            show_compact_toggle=True,
        ),
        # Grid with row grouping support
        create_standard_grid(
            grid_id=_GRID_ID,
            row_data=ComplianceState.filtered_beneficial_ownership,
            column_defs=_get_column_defs(),
            enable_row_numbers=True,  # Tier 2: Row numbering
            enable_multi_select=True,  # Tier 2: Multi-row selection with checkboxes
            default_excel_export_params=get_default_export_params("beneficial_ownership"),
            default_csv_export_params=get_default_csv_export_params("beneficial_ownership"),
            quick_filter_text=BeneficialOwnershipGridState.search_text,
            # Row grouping options
            row_group_panel_show="always",
            group_default_expanded=-1,
        ),
        width="100%",
        height="100%",
        spacing="0",
    )
