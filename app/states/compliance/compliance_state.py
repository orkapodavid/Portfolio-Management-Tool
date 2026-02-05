"""
Compliance State - Module-specific state for Compliance data

Composes all compliance mixins for unified state management.
"""

import reflex as rx
from app.states.compliance.mixins import (
    BeneficialOwnershipMixin,
    MonthlyExerciseLimitMixin,
    RestrictedListMixin,
    UndertakingsMixin,
)


class ComplianceState(
    BeneficialOwnershipMixin,
    MonthlyExerciseLimitMixin,
    RestrictedListMixin,
    UndertakingsMixin,
    rx.State,
):
    """
    Main Compliance module state.
    Inherits from all Compliance subtab mixins to provide unified interface.

    Responsibilities:
    - Load restricted list
    - Load undertakings
    - Load beneficial ownership data
    - Load monthly exercise limits
    - Handle filtering and search for compliance views
    """

    # Module-level state
    active_compliance_subtab: str = "restricted"

    # Shared UI state
    current_search_query: str = ""
    sort_column: str = ""
    sort_direction: str = "asc"
    selected_row: int = -1

    # Legacy loading flag (for backward compatibility)
    is_loading: bool = False

    async def on_load(self):
        """Called when Compliance view loads."""
        await self.load_compliance_data()

    async def load_compliance_data(self):
        """Load all compliance data from services."""
        self.is_loading = True
        try:
            await self.load_restricted_list()
            await self.load_undertakings()
            await self.load_beneficial_ownership()
            await self.load_monthly_exercise_limit()
        except Exception as e:
            import logging

            logging.exception(f"Error loading compliance data: {e}")
        finally:
            self.is_loading = False

    def set_search_query(self, query: str):
        """Update search query for filtering."""
        self.current_search_query = query

    def set_current_tab(self, tab: str):
        """Switch between compliance tabs."""
        self.active_compliance_subtab = tab

    def toggle_sort(self, column: str):
        """Toggle sort direction for a column."""
        if self.sort_column == column:
            self.sort_direction = "desc" if self.sort_direction == "asc" else "asc"
        else:
            self.sort_column = column
            self.sort_direction = "asc"

    def set_selected_row(self, row_id: int):
        """Set selected row ID."""
        self.selected_row = row_id
