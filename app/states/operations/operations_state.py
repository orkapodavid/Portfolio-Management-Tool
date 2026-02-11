"""
Operations State - Module-specific state for Operations data

Composes all operations-related tab mixins:
- Daily Procedure Checks
- Operation Processes
"""

import json
import logging

import reflex as rx
from app.services import OperationsService
from app.states.operations.mixins import (
    DailyProceduresMixin,
    OperationProcessesMixin,
)

logger = logging.getLogger(__name__)


class OperationsState(
    DailyProceduresMixin,
    OperationProcessesMixin,
    rx.State,
):
    """
    State management for operations data.
    Composes all operation tab mixins for unified interface.
    """

    # UI state
    current_tab: str = "daily"

    # Shared UI state for sorting
    sort_column: str = ""
    sort_direction: str = "asc"
    selected_row: int = -1

    async def on_load(self):
        """Called when Operations view loads."""
        await self.load_operations_data()

    async def load_operations_data(self):
        """Load all operations data from mixins."""
        await self.load_daily_procedures_data()
        await self.load_operation_processes_data()

    # =========================================================================
    # Context Menu Handlers
    # =========================================================================

    async def handle_context_menu_action(self, payload_json: str):
        """
        Handle context menu actions dispatched from AG Grid.

        Args:
            payload_json: JSON string with keys 'action' and 'row'.
        """
        try:
            payload = json.loads(payload_json)
        except (json.JSONDecodeError, TypeError):
            logger.warning(f"Invalid context menu payload: {payload_json}")
            return

        action = payload.get("action", "")
        row = payload.get("row", {})
        process_id = row.get("id", 0)
        process_name = row.get("process", row.get("procedure_name", "Unknown"))

        service = OperationsService()

        if action == "Rerun":
            result = await service.rerun_process(process_id, process_name)
            yield rx.toast.success(result["message"], position="top-right")
        elif action == "Kill":
            result = await service.kill_process(process_id, process_name)
            yield rx.toast.warning(result["message"], position="top-right")
        else:
            logger.warning(f"Unknown context menu action: {action}")

    # =========================================================================
    # UI State Methods
    # =========================================================================

    def set_current_tab(self, tab: str):
        """Switch between operations tabs."""
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
