"""
Compliance Mixin - State functionality for Compliance data

This Mixin provides all compliance-related state variables, computed vars,
and event handlers. It integrates with DatabaseService for data access.

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
Pattern: State Mixin for code reuse
"""

import reflex as rx
from app.services import DatabaseService
from app.states.dashboard.types import (
    RestrictedListItem,
    UndertakingItem,
    BeneficialOwnershipItem,
    MonthlyExerciseLimitItem,
)


class ComplianceMixin(rx.State, mixin=True):
    """
    Mixin providing compliance data state and filtering.

    Data provided:
    - Restricted list
    - Undertakings
    - Beneficial ownership
    - Monthly exercise limits
    """

    # Compliance data lists
    restricted_list: list[RestrictedListItem] = []
    undertakings: list[UndertakingItem] = []
    beneficial_ownership: list[BeneficialOwnershipItem] = []
    monthly_exercise_limit: list[MonthlyExerciseLimitItem] = []

    async def load_compliance_data(self):
        """Load all compliance data from DatabaseService."""
        try:
            service = DatabaseService()
            self.restricted_list = await service.get_restricted_list()
            self.undertakings = await service.get_undertakings()
            self.beneficial_ownership = await service.get_beneficial_ownership()
            self.monthly_exercise_limit = await service.get_monthly_exercise_limits()
        except Exception as e:
            import logging

            logging.exception(f"Error loading compliance data: {e}")
