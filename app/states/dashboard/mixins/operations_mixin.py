"""
Operations Mixin - State functionality for Operations data

This Mixin provides all operations-related state variables, computed vars,
and event handlers.

Reference: .agents/skills/reflex-dev/references/reflex-state-structure.mdc
Pattern: State Mixin for code reuse
"""

import reflex as rx
from app.services import DatabaseService
from app.states.dashboard.types import (
    DailyProcedureItem,
    OperationProcessItem,
)


class OperationsMixin(rx.State, mixin=True):
    """
    Mixin providing operations data state and filtering.

    Data provided:
    - Daily procedure checks
    - Operation processes
    """

    # Operations data lists
    daily_procedures: list[DailyProcedureItem] = []
    operation_processes: list[OperationProcessItem] = []

    async def load_operations_data(self):
        """Load all operations data from DatabaseService."""
        try:
            service = DatabaseService()
            self.daily_procedures = await service.get_daily_procedures()
            self.operation_processes = await service.get_operation_processes()
        except Exception as e:
            import logging

            logging.exception(f"Error loading operations data: {e}")
