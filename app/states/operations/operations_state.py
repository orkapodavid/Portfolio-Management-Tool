"""
Operations State - Module-specific state for Operations data

Handles all operations-related data:
- Daily Procedure Checks
- Operation Processes
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.services import DatabaseService
from app.states.operations.types import (
    DailyProcedureItem,
    OperationProcessItem,
)


class OperationsState(rx.State):
    """
    State management for operations data.
    """

    # Operations data lists
    daily_procedures: list[DailyProcedureItem] = []
    operation_processes: list[OperationProcessItem] = []

    # Daily Procedures loading state
    is_loading_daily_procedures: bool = False
    daily_procedures_last_updated: str = "—"

    # Operation Processes loading state
    is_loading_operation_processes: bool = False
    operation_processes_last_updated: str = "—"

    # UI state
    is_loading: bool = False
    current_tab: str = "daily"

    # Shared UI state for sorting
    sort_column: str = ""
    sort_direction: str = "asc"
    selected_row: int = -1

    async def on_load(self):
        """Called when Operations view loads."""
        await self.load_operations_data()

    async def load_operations_data(self):
        """Load all operations data from DatabaseService."""
        self.is_loading = True
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            service = DatabaseService()
            self.daily_procedures = await service.get_daily_procedures()
            self.daily_procedures_last_updated = timestamp

            self.operation_processes = await service.get_operation_processes()
            self.operation_processes_last_updated = timestamp
        except Exception as e:
            import logging

            logging.exception(f"Error loading operations data: {e}")
        finally:
            self.is_loading = False

    # =========================================================================
    # Daily Procedures
    # =========================================================================

    async def force_refresh_daily_procedures(self):
        """Force refresh daily procedures with loading overlay."""
        if self.is_loading_daily_procedures:
            return
        self.is_loading_daily_procedures = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = DatabaseService()
            self.daily_procedures = await service.get_daily_procedures()
            self.daily_procedures_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing daily procedures: {e}")
        finally:
            self.is_loading_daily_procedures = False

    # =========================================================================
    # Operation Processes
    # =========================================================================

    async def force_refresh_operation_processes(self):
        """Force refresh operation processes with loading overlay."""
        if self.is_loading_operation_processes:
            return
        self.is_loading_operation_processes = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = DatabaseService()
            self.operation_processes = await service.get_operation_processes()
            self.operation_processes_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing operation processes: {e}")
        finally:
            self.is_loading_operation_processes = False

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
