"""
Risk Mixin - State functionality for Risk data

This Mixin provides all risk-related state variables, computed vars,
and event handlers. It integrates with RiskService for data access.

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
Pattern: State Mixin for code reuse
"""

import reflex as rx
from app.services import RiskService
from app.states.dashboard.types import (
    DeltaChangeItem,
    RiskMeasureItem,
    RiskInputItem,
)


class RiskMixin(rx.State, mixin=True):
    """
    Mixin providing risk data state and filtering.

    Data provided:
    - Delta changes
    - Risk measures
    - Risk inputs
    """

    # Risk data lists
    delta_changes: list[DeltaChangeItem] = []
    risk_measures: list[RiskMeasureItem] = []
    risk_inputs: list[RiskInputItem] = []

    async def load_risk_data(self):
        """Load all risk data from RiskService."""
        try:
            service = RiskService()
            self.delta_changes = await service.get_delta_changes()
            self.risk_measures = await service.get_risk_measures()
            self.risk_inputs = await service.get_risk_inputs()
        except Exception as e:
            import logging

            logging.exception(f"Error loading risk data: {e}")

    def _filter_risk_by_ticker(
        self, items: list[dict], search_query: str
    ) -> list[dict]:
        """Helper to filter risk items by ticker or company name."""
        if not search_query:
            return items
        query = search_query.lower()
        return [
            item
            for item in items
            if query in item.get("ticker", "").lower()
            or query in item.get("company_name", "").lower()
        ]
