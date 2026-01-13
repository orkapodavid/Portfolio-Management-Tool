"""
Compliance State - Module-specific state for Compliance data

Handles all compliance-related data and calculations.
"""

import reflex as rx
from app.services import ComplianceService
from app.states.compliance.types import (
    RestrictedListItem,
    UndertakingItem,
    BeneficialOwnershipItem,
    MonthlyExerciseLimitItem,
)


class ComplianceState(rx.State):
    """
    State management for compliance and regulatory data.

    Responsibilities:
    - Load restricted list
    - Load undertakings
    - Load beneficial ownership data
    - Load monthly exercise limits
    - Handle filtering and search for compliance views
    """

    # Data storage
    restricted_list: list[RestrictedListItem] = []
    undertakings: list[UndertakingItem] = []
    beneficial_ownership: list[BeneficialOwnershipItem] = []
    monthly_exercise_limit: list[MonthlyExerciseLimitItem] = []

    # UI state
    is_loading: bool = False
    current_search_query: str = ""
    current_tab: str = "restricted"

    # Shared UI state for sorting
    sort_column: str = ""
    sort_direction: str = "asc"
    selected_row: int = -1

    async def on_load(self):
        """Called when Compliance view loads."""
        await self.load_compliance_data()

    async def load_compliance_data(self):
        """Load compliance data from ComplianceService."""
        self.is_loading = True
        try:
            service = ComplianceService()
            self.restricted_list = await service.get_restricted_list()
            self.undertakings = await service.get_undertakings()
            self.beneficial_ownership = await service.get_beneficial_ownership()
            self.monthly_exercise_limit = await service.get_monthly_exercise_limit()
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
        self.current_tab = tab

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

    @rx.var(cache=True)
    def filtered_restricted_list(self) -> list[RestrictedListItem]:
        """Filtered restricted list based on search query."""
        if not self.current_search_query:
            return self.restricted_list

        query = self.current_search_query.lower()
        return [
            item
            for item in self.restricted_list
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_undertakings(self) -> list[UndertakingItem]:
        """Filtered undertakings based on search query."""
        if not self.current_search_query:
            return self.undertakings

        query = self.current_search_query.lower()
        return [
            item
            for item in self.undertakings
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
            or query in item.get("deal_num", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_beneficial_ownership(self) -> list[BeneficialOwnershipItem]:
        """Filtered beneficial ownership based on search query."""
        if not self.current_search_query:
            return self.beneficial_ownership

        query = self.current_search_query.lower()
        return [
            item
            for item in self.beneficial_ownership
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_monthly_exercise_limit(self) -> list[MonthlyExerciseLimitItem]:
        """Filtered monthly exercise limit based on search query."""
        if not self.current_search_query:
            return self.monthly_exercise_limit

        query = self.current_search_query.lower()
        return [
            item
            for item in self.monthly_exercise_limit
            if query in item.get("ticker", "").lower()
            or query in item.get("underlying", "").lower()
        ]
