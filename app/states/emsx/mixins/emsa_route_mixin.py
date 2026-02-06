"""Mixin for EMSA Route grid state with auto-refresh (ticking) pattern."""

import asyncio
import random
from datetime import datetime

import reflex as rx
from app.services import EMSXService


class EMSARouteMixin(rx.State, mixin=True):
    """
    Mixin providing EMSA Routes data state and auto-refresh pattern.

    Implements the Ticking pattern for real-time route updates:
    - Auto-refresh background task
    - Loading overlay for force refresh
    - Simulated updates for demo mode
    """

    # EMSA Routes data
    emsa_routes: list[dict] = []
    is_loading_emsa_routes: bool = False
    emsa_route_last_updated: str = "—"
    emsa_route_auto_refresh: bool = True

    async def load_emsa_routes(self):
        """Load EMSA routes from EMSXService."""
        self.is_loading_emsa_routes = True
        try:
            service = EMSXService()
            self.emsa_routes = await service.get_emsx_routes()
            self.emsa_route_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            import logging

            logging.exception(f"Error loading EMSA routes: {e}")
        finally:
            self.is_loading_emsa_routes = False

    def toggle_emsa_route_auto_refresh(self, value: bool):
        """Toggle auto-refresh for EMSA routes."""
        self.emsa_route_auto_refresh = value
        if value:
            return type(self).start_emsa_route_auto_refresh

    @rx.event(background=True)
    async def start_emsa_route_auto_refresh(self):
        """Background task for EMSA route auto-refresh."""
        while True:
            async with self:
                if not self.emsa_route_auto_refresh:
                    break
                self.simulate_emsa_route_update()
            await asyncio.sleep(2)  # Update every 2 seconds

    def simulate_emsa_route_update(self):
        """Simulate route fill updates (for demo/mock mode)."""
        if not self.emsa_routes:
            return
        
        # Create a NEW list (required for change detection)
        new_list = list(self.emsa_routes)
        
        # Pick a random route and update its filled quantity
        idx = random.randint(0, len(new_list) - 1)
        
        # Create a NEW row dict (required for cell flash)
        route = dict(new_list[idx])
        
        # Parse and update filled quantity
        try:
            current_filled = int(route.get("filled_quantity", 0))
            new_filled = current_filled + random.randint(50, 500)
            route["filled_quantity"] = new_filled
        except (ValueError, TypeError):
            route["filled_quantity"] = random.randint(500, 3000)
        
        # Replace the row in the new list
        new_list[idx] = route
        
        # Assign new list to state (triggers change detection)
        self.emsa_routes = new_list
        self.emsa_route_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_emsa_routes(self):
        """Force refresh EMSA routes with loading overlay."""
        if self.is_loading_emsa_routes:
            return  # Debounce
        self.is_loading_emsa_routes = True
        yield  # Send loading state to client immediately
        await asyncio.sleep(0.3)
        try:
            service = EMSXService()
            self.emsa_routes = await service.get_emsx_routes()
            self.emsa_route_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            import logging

            logging.exception(f"Error refreshing EMSA routes: {e}")
        finally:
            self.is_loading_emsa_routes = False
