"""
Operation Processes Mixin - Tab-specific state for Operation Processes.

Provides auto-refresh background task and force refresh functionality.
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.services import OperationsService
from app.states.operations.types import OperationProcessItem
import logging
import random

class OperationProcessesMixin(rx.State, mixin=True):
    """
    Mixin providing Operation Processes data state with auto-refresh.
    """

    # Operation Processes data
    operation_processes: list[OperationProcessItem] = []
    is_loading_operation_processes: bool = False
    operation_processes_last_updated: str = "—"
    operation_processes_auto_refresh: bool = True

    async def load_operation_processes_data(self):
        """Load Operation Processes data from OperationsService."""
        self.is_loading_operation_processes = True
        try:
            service = OperationsService()
            self.operation_processes = await service.get_operation_processes()
            self.operation_processes_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error loading operation processes data: {e}")
        finally:
            self.is_loading_operation_processes = False

    @rx.event(background=True)
    async def start_operation_processes_auto_refresh(self):
        """Background task for Operation Processes auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.operation_processes_auto_refresh:
                    break
                self.simulate_operation_processes_update()
            await asyncio.sleep(2)

    def toggle_operation_processes_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.operation_processes_auto_refresh = value
        if value:
            return type(self).start_operation_processes_auto_refresh

    def simulate_operation_processes_update(self):
        """Simulated delta update for demo - random status/time changes."""
        if (
            not self.operation_processes_auto_refresh
            or len(self.operation_processes) < 1
        ):
            return

        new_list = list(self.operation_processes)

        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            new_row = dict(old_row)

            # Simulate status changes
            if "status" in new_row:
                statuses = ["Idle", "Running", "Completed", "Error"]
                if random.random() > 0.8:
                    new_row["status"] = random.choice(statuses)

            # Update last_run_time
            if "last_run_time" in new_row:
                new_row["last_run_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            new_list[idx] = new_row

        self.operation_processes = new_list
        self.operation_processes_last_updated = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    async def force_refresh_operation_processes(self):
        """Force refresh operation processes with loading overlay."""
        if self.is_loading_operation_processes:
            return
        self.is_loading_operation_processes = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = OperationsService()
            self.operation_processes = await service.get_operation_processes()
            self.operation_processes_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error refreshing operation processes: {e}")
        finally:
            self.is_loading_operation_processes = False
