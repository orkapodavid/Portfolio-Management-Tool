"""Mixin for EMSA Order grid state with auto-refresh (ticking) pattern."""

import asyncio
import random
from datetime import datetime

import reflex as rx
from app.services import EMSXService
from app.states.types import EMSAOrderItem


class EMSAOrderMixin(rx.State, mixin=True):
    """
    Mixin providing EMSA Orders data state and auto-refresh pattern.

    Implements the Ticking pattern for real-time order updates:
    - Auto-refresh background task
    - Loading overlay for force refresh
    - Simulated updates for demo mode
    """

    # EMSA Orders data
    emsa_orders: list[EMSAOrderItem] = []
    is_loading_emsa_orders: bool = False
    emsa_order_last_updated: str = "—"
    emsa_order_auto_refresh: bool = True

    async def load_emsa_orders(self):
        """Load EMSA orders from EMSXService."""
        self.is_loading_emsa_orders = True
        try:
            service = EMSXService()
            self.emsa_orders = await service.get_emsx_orders()
            self.emsa_order_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            import logging

            logging.exception(f"Error loading EMSA orders: {e}")
        finally:
            self.is_loading_emsa_orders = False

    def toggle_emsa_order_auto_refresh(self, value: bool):
        """Toggle auto-refresh for EMSA orders."""
        self.emsa_order_auto_refresh = value
        if value:
            return type(self).start_emsa_order_auto_refresh

    @rx.event(background=True)
    async def start_emsa_order_auto_refresh(self):
        """Background task for EMSA order auto-refresh."""
        while True:
            async with self:
                if not self.emsa_order_auto_refresh:
                    break
                self.simulate_emsa_order_update()
            await asyncio.sleep(2)  # Update every 2 seconds

    def simulate_emsa_order_update(self):
        """Simulate order fill updates (for demo/mock mode)."""
        if not self.emsa_orders:
            return
        
        # Create a NEW list (required for change detection)
        new_list = list(self.emsa_orders)
        
        # Pick a random order and update its filled quantity
        idx = random.randint(0, len(new_list) - 1)
        
        # Create a NEW row dict (required for cell flash)
        order = dict(new_list[idx])
        
        # Parse and update filled amount
        try:
            current_filled_str = str(order.get("emsa_filled", "0"))
            current_filled = int(current_filled_str.replace(",", ""))
            new_filled = current_filled + random.randint(100, 1000)
            order["emsa_filled"] = f"{new_filled:,}"
        except (ValueError, TypeError):
            order["emsa_filled"] = f"{random.randint(1000, 5000):,}"
        
        # Replace the row in the new list
        new_list[idx] = order
        
        # Assign new list to state (triggers change detection)
        self.emsa_orders = new_list
        self.emsa_order_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_emsa_orders(self):
        """Force refresh EMSA orders with loading overlay."""
        if self.is_loading_emsa_orders:
            return  # Debounce
        self.is_loading_emsa_orders = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.3)
        try:
            service = EMSXService()
            self.emsa_orders = await service.get_emsx_orders()
            self.emsa_order_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing EMSA orders: {e}")
        finally:
            self.is_loading_emsa_orders = False
