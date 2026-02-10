"""
EMSX Service for Portfolio Management Tool.

Delegates all data methods to pmt_core.services.emsx.EMSXService.
"""

import logging
from typing import Optional

from pmt_core.services.emsx import EMSXService as CoreEMSXService

logger = logging.getLogger(__name__)


class EMSXService:
    """
    Service for Bloomberg EMSX order management.
    Delegates to pmt_core EMSXService for data.
    """

    def __init__(self):
        self.core_service = CoreEMSXService()

    async def get_emsx_orders(self, status_filter: Optional[str] = None) -> list[dict]:
        """Get EMSX orders. Delegates to core."""
        return await self.core_service.get_emsx_orders(status_filter)

    async def get_emsx_routes(self, order_id: Optional[int] = None) -> list[dict]:
        """Get EMSX routes. Delegates to core."""
        return await self.core_service.get_emsx_routes(order_id)

    async def create_emsx_order(self, order_params: dict) -> dict:
        """Create a new EMSX order. Delegates to core."""
        return await self.core_service.create_emsx_order(order_params)

    async def cancel_emsx_order(self, order_id: int) -> dict:
        """Cancel an EMSX order. Delegates to core."""
        return await self.core_service.cancel_emsx_order(order_id)

    async def modify_emsx_order(self, order_id: int, modifications: dict) -> dict:
        """Modify an EMSX order. Delegates to core."""
        return await self.core_service.modify_emsx_order(order_id, modifications)

    async def subscribe_to_orders(self, callback_fn=None) -> bool:
        """Subscribe to order updates. Delegates to core."""
        return await self.core_service.subscribe_to_orders(callback_fn)
