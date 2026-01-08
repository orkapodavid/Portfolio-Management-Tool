"""
Compliance State - Portfolio Dashboard Substate

Handles all compliance and regulatory data for the portfolio dashboard.

This follows Reflex best practices for state architecture:
- Focused responsibility (only compliance data)
- Service integration (uses DatabaseService)
- Independent from other dashboard states
- Efficient loading (only loads when needed)

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
Pattern: Flat state structure with focused substates

Created as part of portfolio_dashboard_state.py restructuring.
"""

import reflex as rx
from app.services import DatabaseService
from app.states.dashboard.types import (
    RestrictedListItem,
    UndertakingItem,
    BeneficialOwnershipItem,
)


class ComplianceState(rx.State):
    """
    State management for compliance and regulatory data.

    Responsibilities:
    - Load restricted list
    - Load undertakings
    - Load beneficial ownership data
    - Handle filtering and search for compliance views

    Best Practices Applied:
    1. Single Responsibility: Only handles compliance data
    2. Service Integration: Uses DatabaseService for data access
    3. Independent State: Doesn't inherit from other states
    4. Async Loading: Loads data asynchronously on demand
    """

    # Data storage
    restricted_list: list[RestrictedListItem] = []
    undertakings: list[UndertakingItem] = []
    beneficial_ownership: list[BeneficialOwnershipItem] = []

    # UI state
    is_loading: bool = False
    current_search_query: str = ""
    current_tab: str = "restricted"  # "restricted", "undertakings", "ownership"

    async def on_load(self):
        """
        Called when Compliance view loads.

        Best Practice: Use on_load for initial data fetching.
        """
        await self.load_compliance_data()

    async def load_compliance_data(self):
        """
        Load compliance data from DatabaseService.

        Service Integration Pattern:
        1. Set loading state
        2. Instantiate service
        3. Call service methods
        4. Update state with results
        5. Clear loading state
        """
        self.is_loading = True
        try:
            service = DatabaseService()

            # Load compliance data from database
            # TODO: Implement actual database queries
            # self.restricted_list = await service.execute_query(
            #     "SELECT * FROM restricted_list WHERE active = 1"
            # )
            # self.undertakings = await service.execute_query(
            #     "SELECT * FROM undertakings WHERE status = 'active'"
            # )
            # self.beneficial_ownership = await service.execute_query(
            #     "SELECT * FROM beneficial_ownership ORDER BY trade_date DESC"
            # )

            # For now, using empty lists (replaced by real queries above)
            self.restricted_list = []
            self.undertakings = []
            self.beneficial_ownership = []

        except Exception as e:
            import logging

            logging.exception(f"Error loading compliance data: {e}")
        finally:
            self.is_loading = False

    @rx.event
    def set_search_query(self, query: str):
        """Update search query for filtering."""
        self.current_search_query = query

    @rx.event
    def set_current_tab(self, tab: str):
        """Switch between compliance tabs."""
        self.current_tab = tab

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

    @rx.var
    def restricted_count(self) -> int:
        """Total count of restricted securities."""
        return len(self.restricted_list)

    @rx.var
    def active_undertakings_count(self) -> int:
        """Count of active undertakings."""
        return len(self.undertakings)
