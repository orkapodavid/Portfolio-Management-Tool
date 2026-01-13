"""
Operations State - Module-specific state for Operations data

Handles all operations-related data:
- Daily Procedure Checks
- Operation Processes
"""

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

    # UI state
    is_loading: bool = False
    current_search_query: str = ""
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
        try:
            service = DatabaseService()
            self.daily_procedures = await service.get_daily_procedures()
            self.operation_processes = await service.get_operation_processes()
        except Exception as e:
            import logging

            logging.exception(f"Error loading operations data: {e}")
        finally:
            self.is_loading = False

    def set_search_query(self, query: str):
        """Update search query for filtering."""
        self.current_search_query = query

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

    @rx.var(cache=True)
    def filtered_daily_procedures(self) -> list[DailyProcedureItem]:
        """Filtered daily procedures based on search query."""
        if not self.current_search_query:
            return self.daily_procedures

        query = self.current_search_query.lower()
        return [
            item
            for item in self.daily_procedures
            if query in item.get("procedure_name", "").lower()
            or query in item.get("status", "").lower()
        ]

    @rx.var(cache=True)
    def filtered_operation_processes(self) -> list[OperationProcessItem]:
        """Filtered operation processes based on search query."""
        if not self.current_search_query:
            return self.operation_processes

        query = self.current_search_query.lower()
        return [
            item
            for item in self.operation_processes
            if query in item.get("process", "").lower()
            or query in item.get("status", "").lower()
        ]
