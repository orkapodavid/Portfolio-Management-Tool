"""
Compliance Service - Handles compliance and regulatory data.

Delegates to pmt_core.services.ComplianceService.
"""

import logging
from pmt_core.services import ComplianceService as CoreComplianceService
from pmt_core import ComplianceRecord

logger = logging.getLogger(__name__)


class ComplianceService:
    """Service for compliance and regulatory data retrieval."""

    def __init__(self):
        self.core_service = CoreComplianceService()

    async def get_restricted_list(self) -> list[ComplianceRecord]:
        """Get restricted securities list."""
        return await self.core_service.get_restricted_list()

    async def get_undertakings(self) -> list[ComplianceRecord]:
        """Get undertakings data."""
        return await self.core_service.get_undertakings()

    async def get_beneficial_ownership(self) -> list[ComplianceRecord]:
        """Get beneficial ownership data."""
        return await self.core_service.get_beneficial_ownership()

    async def get_monthly_exercise_limit(self) -> list[dict]:
        """Get monthly exercise limit data."""
        return await self.core_service.get_monthly_exercise_limit()
