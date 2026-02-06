"""
Reverse Inquiry Mixin - Tab-specific state for Reverse Inquiry data.

Provides auto-refresh background task and force refresh functionality.
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.services import DatabaseService
from app.states.events.types import ReverseInquiryItem


class ReverseInquiryMixin(rx.State, mixin=True):
    """
    Mixin providing Reverse Inquiry data state with auto-refresh.
    """

    # Reverse Inquiry data
    reverse_inquiry: list[ReverseInquiryItem] = []
    is_loading_reverse_inquiry: bool = False
    reverse_inquiry_last_updated: str = "—"
    reverse_inquiry_auto_refresh: bool = True

    async def load_reverse_inquiry_data(self):
        """Load Reverse Inquiry data from DatabaseService."""
        self.is_loading_reverse_inquiry = True
        try:
            service = DatabaseService()
            self.reverse_inquiry = await service.get_reverse_inquiry()
            self.reverse_inquiry_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error loading reverse inquiry data: {e}")
        finally:
            self.is_loading_reverse_inquiry = False

    @rx.event(background=True)
    async def start_reverse_inquiry_auto_refresh(self):
        """Background task for Reverse Inquiry auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.reverse_inquiry_auto_refresh:
                    break
                self.simulate_reverse_inquiry_update()
            await asyncio.sleep(2)

    def toggle_reverse_inquiry_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.reverse_inquiry_auto_refresh = value
        if value:
            return type(self).start_reverse_inquiry_auto_refresh

    def simulate_reverse_inquiry_update(self):
        """Simulated delta update for demo - random deal point changes."""
        if not self.reverse_inquiry_auto_refresh or len(self.reverse_inquiry) < 1:
            return

        import random

        # Create a new list to trigger change detection
        new_list = list(self.reverse_inquiry)

        # Update 1-3 random rows
        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            # Create a new row dict (immutable update for AG Grid change detection)
            new_row = dict(old_row)

            # Simulate deal_point changes
            if "deal_point" in new_row and new_row["deal_point"]:
                try:
                    # Parse the value and add small random change
                    val_str = str(new_row["deal_point"]).replace("%", "").replace(",", "")
                    val = float(val_str)
                    new_val = round(val * random.uniform(0.98, 1.02), 2)
                    new_row["deal_point"] = f"{new_val:.2f}%"
                except (ValueError, TypeError):
                    pass

            new_list[idx] = new_row

        self.reverse_inquiry = new_list
        self.reverse_inquiry_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_reverse_inquiry(self):
        """Force refresh reverse inquiry data with loading overlay."""
        if self.is_loading_reverse_inquiry:
            return  # Debounce
        self.is_loading_reverse_inquiry = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.3)
        try:
            service = DatabaseService()
            self.reverse_inquiry = await service.get_reverse_inquiry()
            self.reverse_inquiry_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing reverse inquiry: {e}")
        finally:
            self.is_loading_reverse_inquiry = False
