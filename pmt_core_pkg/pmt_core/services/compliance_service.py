from typing import List, Optional
from ..repositories.compliance_repository import ComplianceRepository
from ..models import ComplianceRecord
import logging

logger = logging.getLogger(__name__)


class ComplianceService:
    """
    Core business service for Compliance.
    Delegates data fetching to ComplianceRepository.
    """

    def __init__(self, repository: Optional[ComplianceRepository] = None):
        self.repository = repository or ComplianceRepository()

    async def get_restricted_list(self) -> List[ComplianceRecord]:
        """Get restricted list."""
        return await self.repository.get_restricted_list()

    async def get_undertakings(self) -> List[ComplianceRecord]:
        """Get undertakings."""
        return await self.repository.get_undertakings()

    async def get_beneficial_ownership(self) -> List[ComplianceRecord]:
        """Get beneficial ownership."""
        return await self.repository.get_beneficial_ownership()

    async def get_monthly_exercise_limit(self) -> List[dict]:
        """Get monthly exercise limits."""
        return await self.repository.get_monthly_exercise_limits()
