"""Mixin for EMSX Order grid state with auto-refresh (ticking) pattern."""

import asyncio
import random
from datetime import datetime

import reflex as rx
from app.services import EMSXService
from app.states.types import EMSXOrderItem


class EMSXOrderMixin(rx.State, mixin=True):
    """
    Mixin providing EMSX Orders data state and auto-refresh pattern.

    Implements the Ticking pattern for real-time order updates:
    - Auto-refresh background task
    - Loading overlay for force refresh
    - Simulated updates for demo mode
    """

    # EMSX Orders data
    emsx_orders: list[EMSXOrderItem] = []
    is_loading_emsx_orders: bool = False
    emsx_order_last_updated: str = "—"
    emsx_order_auto_refresh: bool = True

    async def load_emsx_orders(self):
        """Load EMSX orders from EMSXService."""
        self.is_loading_emsx_orders = True
        try:
            service = EMSXService()
            self.emsx_orders = await service.get_emsx_orders()
            self.emsx_order_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            import logging

            logging.exception(f"Error loading EMSX orders: {e}")
        finally:
            self.is_loading_emsx_orders = False

    def toggle_emsx_order_auto_refresh(self, value: bool):
        """Toggle auto-refresh for EMSX orders."""
        self.emsx_order_auto_refresh = value
        if value:
            return type(self).start_emsx_order_auto_refresh

    @rx.event(background=True)
    async def start_emsx_order_auto_refresh(self):
        """Background task for EMSX order auto-refresh."""
        while True:
            async with self:
                if not self.emsx_order_auto_refresh:
                    break
                self.simulate_emsx_order_update()
            await asyncio.sleep(2)  # Update every 2 seconds

    def simulate_emsx_order_update(self):
        """Simulate order fill updates (for demo/mock mode)."""
        if not self.emsx_orders:
            return
        
        # Create a NEW list (required for change detection)
        new_list = list(self.emsx_orders)
        
        # Pick a random order and update its filled quantity
        idx = random.randint(0, len(new_list) - 1)
        
        # Create a NEW row dict (required for cell flash)
        order = dict(new_list[idx])
        
        # Parse and update filled amount
        try:
            current_filled_str = str(order.get("emsx_filled", "0"))
            current_filled = int(current_filled_str.replace(",", ""))
            new_filled = current_filled + random.randint(100, 1000)
            order["emsx_filled"] = f"{new_filled:,}"
        except (ValueError, TypeError):
            order["emsx_filled"] = f"{random.randint(1000, 5000):,}"
        
        # Replace the row in the new list
        new_list[idx] = order
        
        # Assign new list to state (triggers change detection)
        self.emsx_orders = new_list
        self.emsx_order_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_emsx_orders(self):
        """Force refresh EMSX orders with loading overlay."""
        if self.is_loading_emsx_orders:
            return  # Debounce
        self.is_loading_emsx_orders = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.3)
        try:
            service = EMSXService()
            self.emsx_orders = await service.get_emsx_orders()
            self.emsx_order_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing EMSX orders: {e}")
        finally:
            self.is_loading_emsx_orders = False