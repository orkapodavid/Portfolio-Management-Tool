"""
EMSX Mixin - State functionality for EMSX/Orders data

This Mixin provides all EMSX/orders-related state variables, computed vars,
and event handlers. It integrates with EMSXService for data access.

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
Pattern: State Mixin for code reuse
"""

import reflex as rx
from app.services import EMSXService
from app.states.dashboard.types import EMSAOrderItem


class EMSXMixin(rx.State, mixin=True):
    """
    Mixin providing EMSX/orders data state and filtering.

    Data provided:
    - EMSX orders
    - EMSX routes
    """

    # EMSA data lists
    emsa_orders: list[EMSAOrderItem] = []
    emsa_routes: list[dict] = []

    async def load_emsa_data(self):
        """Load all EMSA data from EMSXService."""
        try:
            service = EMSXService()
            self.emsa_orders = await service.get_emsx_orders()
            self.emsa_routes = await service.get_emsx_routes()
        except Exception as e:
            import logging

            logging.exception(f"Error loading EMSX data: {e}")
