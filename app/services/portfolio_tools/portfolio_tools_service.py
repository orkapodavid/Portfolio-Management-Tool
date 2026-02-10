"""
Portfolio Tools Service for Portfolio Management Tool.

Delegates all data methods to pmt_core.services.portfolio_tools.PortfolioToolsService.
"""

import logging
from typing import Optional

from pmt_core.services.portfolio_tools import (
    PortfolioToolsService as CorePortfolioToolsService,
)

logger = logging.getLogger(__name__)


class PortfolioToolsService:
    """
    Service for managing portfolio tools data.
    Delegates to pmt_core PortfolioToolsService for data.
    """

    def __init__(self):
        self.core_service = CorePortfolioToolsService()

    async def get_portfolios(self, user_id: str = None) -> list[dict]:
        """Get all portfolios. Delegates to core."""
        return await self.core_service.get_portfolios(user_id)

    async def get_portfolio(self, portfolio_id: str) -> dict:
        """Get a specific portfolio. Delegates to core."""
        return await self.core_service.get_portfolio(portfolio_id)

    async def create_portfolio(self, portfolio_data: dict) -> dict:
        """Create a new portfolio. Delegates to core."""
        return await self.core_service.create_portfolio(portfolio_data)

    async def add_transaction(self, portfolio_id: str, transaction_data: dict) -> dict:
        """Add a transaction. Delegates to core."""
        return await self.core_service.add_transaction(portfolio_id, transaction_data)

    async def get_transactions(self, portfolio_id: str, limit: int = 100) -> list[dict]:
        """Get transactions. Delegates to core."""
        return await self.core_service.get_transactions(portfolio_id, limit)

    async def add_dividend(self, portfolio_id: str, dividend_data: dict) -> dict:
        """Record a dividend. Delegates to core."""
        return await self.core_service.add_dividend(portfolio_id, dividend_data)

    async def get_dividends(self, portfolio_id: str, limit: int = 100) -> list[dict]:
        """Get dividends. Delegates to core."""
        return await self.core_service.get_dividends(portfolio_id, limit)

    async def update_portfolio_cash(
        self, portfolio_id: str, cash_amount: float
    ) -> bool:
        """Update cash balance. Delegates to core."""
        return await self.core_service.update_portfolio_cash(portfolio_id, cash_amount)

    async def get_pay_to_hold(self) -> list[dict]:
        """Get pay-to-hold data. Delegates to core."""
        return await self.core_service.get_pay_to_hold()

    async def get_short_ecl(self) -> list[dict]:
        """Get short ECL data. Delegates to core."""
        return await self.core_service.get_short_ecl()

    async def get_stock_borrow(self) -> list[dict]:
        """Get stock borrow data. Delegates to core."""
        return await self.core_service.get_stock_borrow()

    async def get_po_settlement(self) -> list[dict]:
        """Get PO settlement data. Delegates to core."""
        return await self.core_service.get_po_settlement()

    async def get_deal_indication(self) -> list[dict]:
        """Get deal indication data. Delegates to core."""
        return await self.core_service.get_deal_indication()

    async def get_reset_dates(self) -> list[dict]:
        """Get reset dates data. Delegates to core."""
        return await self.core_service.get_reset_dates()

    async def get_coming_resets(self) -> list[dict]:
        """Get coming resets data. Delegates to core."""
        return await self.core_service.get_coming_resets()

    async def get_cb_installments(self) -> list[dict]:
        """Get CB installments data. Delegates to core."""
        return await self.core_service.get_cb_installments()

    async def get_excess_amount(self) -> list[dict]:
        """Get excess amount data. Delegates to core."""
        return await self.core_service.get_excess_amount()
