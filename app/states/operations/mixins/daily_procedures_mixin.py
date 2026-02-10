"""
Daily Procedures Mixin - Tab-specific state for Daily Procedure Checks.

Provides auto-refresh background task and force refresh functionality.
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.services import OperationsService
from app.states.operations.types import DailyProcedureItem


class DailyProceduresMixin(rx.State, mixin=True):
    """
    Mixin providing Daily Procedures data state with auto-refresh.
    """

    # Daily Procedures data
    daily_procedures: list[DailyProcedureItem] = []
    is_loading_daily_procedures: bool = False
    daily_procedures_last_updated: str = "—"
    daily_procedures_auto_refresh: bool = True

    async def load_daily_procedures_data(self):
        """Load Daily Procedures data from OperationsService."""
        self.is_loading_daily_procedures = True
        try:
            service = OperationsService()
            self.daily_procedures = await service.get_daily_procedures()
            self.daily_procedures_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error loading daily procedures data: {e}")
        finally:
            self.is_loading_daily_procedures = False

    @rx.event(background=True)
    async def start_daily_procedures_auto_refresh(self):
        """Background task for Daily Procedures auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.daily_procedures_auto_refresh:
                    break
                self.simulate_daily_procedures_update()
            await asyncio.sleep(2)

    def toggle_daily_procedures_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.daily_procedures_auto_refresh = value
        if value:
            return type(self).start_daily_procedures_auto_refresh

    def simulate_daily_procedures_update(self):
        """Simulated delta update for demo - random status changes."""
        if not self.daily_procedures_auto_refresh or len(self.daily_procedures) < 1:
            return

        import random

        new_list = list(self.daily_procedures)

        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            new_row = dict(old_row)

            # Simulate status changes
            if "status" in new_row:
                statuses = ["Pending", "Running", "Completed", "Failed"]
                current_status = new_row.get("status", "Pending")
                if current_status in statuses:
                    # Move to next status with some probability
                    if random.random() > 0.7:
                        current_idx = statuses.index(current_status)
                        if current_idx < len(statuses) - 2:
                            new_row["status"] = statuses[current_idx + 1]

            new_list[idx] = new_row

        self.daily_procedures = new_list
        self.daily_procedures_last_updated = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    async def force_refresh_daily_procedures(self):
        """Force refresh daily procedures with loading overlay."""
        if self.is_loading_daily_procedures:
            return
        self.is_loading_daily_procedures = True
        yield
        await asyncio.sleep(0.3)
        try:
            service = OperationsService()
            self.daily_procedures = await service.get_daily_procedures()
            self.daily_procedures_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing daily procedures: {e}")
        finally:
            self.is_loading_daily_procedures = False
