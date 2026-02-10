"""
Instruments Service — core business logic for instruments data.

Provides mock data for stock screener, ticker data, special terms,
instrument data, and instrument terms.
TODO: Replace mock data with actual database/repository calls.
"""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class InstrumentsService:
    """
    Service for managing instruments data.

    Generates mock instruments data.
    Real implementation would delegate to a repository layer.
    """

    async def get_stock_screener(self) -> list[dict[str, Any]]:
        """Get stock screener data. TODO: Replace with DB query."""
        logger.info("Returning mock stock screener data")
        return [
            {
                "id": 1,
                "otl": "1",
                "mkt_cap_37_pct": "12.5%",
                "ticker": "AAPL",
                "company": "Apple Inc.",
                "country": "USA",
                "industry": "Technology",
                "last_price": "182.50",
                "mkt_cap_loc": "2.95T",
                "mkt_cap_usd": "2.95T",
                "adv_3m": "54.2M",
                "locate_qty_mm": "100",
                "locate_f": "Y",
            },
            {
                "id": 2,
                "otl": "2",
                "mkt_cap_37_pct": "10.2%",
                "ticker": "MSFT",
                "company": "Microsoft Corp.",
                "country": "USA",
                "industry": "Technology",
                "last_price": "405.12",
                "mkt_cap_loc": "3.01T",
                "mkt_cap_usd": "3.01T",
                "adv_3m": "22.4M",
                "locate_qty_mm": "80",
                "locate_f": "Y",
            },
        ]

    async def get_ticker_data(self) -> list[dict[str, Any]]:
        """Get ticker data for instruments. TODO: Replace with DB query."""
        logger.info("Returning mock ticker data")
        tickers = ["AAPL", "MSFT", "TSLA", "NVDA", "GOOGL", "META", "AMZN", "AMD"]
        sectors = [
            "Technology",
            "Technology",
            "Automotive",
            "Technology",
            "Technology",
            "Technology",
            "Consumer",
            "Technology",
        ]
        return [
            {
                "id": i + 1,
                "ticker": tickers[i],
                "currency": "USD",
                "fx_rate": "1.0000",
                "sector": sectors[i],
                "company": f"{tickers[i]} Inc.",
                "po_lead_manager": [
                    "Goldman Sachs",
                    "Morgan Stanley",
                    "JP Morgan",
                    "Citibank",
                ][i % 4],
                "fmat_cap": f"${(2.5 + i * 0.3):.2f}T",
                "smkt_cap": f"${(2.5 + i * 0.3):.2f}T",
                "chg_1d_pct": f"{(-1.5 + i * 0.5):.2f}%",
                "dtl": f"{30 + i * 5}",
            }
            for i in range(len(tickers))
        ]

    async def get_special_terms(self) -> list[dict[str, Any]]:
        """Get special terms data. TODO: Replace with DB query."""
        logger.info("Returning mock special terms data")
        return [
            {
                "id": 1,
                "deal_num": "D001",
                "ticker": "AAPL",
                "company_name": "Apple Inc.",
                "sec_type": "Equity",
                "pos_loc": "US",
                "account": "Main Account",
                "effective_date": "2025-01-01",
                "position": "10,000",
            },
        ]

    async def get_instrument_data(self) -> list[dict[str, Any]]:
        """Get instrument data. TODO: Replace with DB query."""
        logger.info("Returning mock instrument data")
        return [
            {
                "id": 1,
                "deal_num": "D001",
                "detail_id": "DT001",
                "underlying": "AAPL",
                "ticker": "AAPL",
                "company_name": "Apple Inc.",
                "sec_id": "SEC001",
                "sec_type": "Equity",
                "pos_loc": "US",
                "account": "Main Account",
            },
            {
                "id": 2,
                "deal_num": "D002",
                "detail_id": "DT002",
                "underlying": "MSFT",
                "ticker": "MSFT",
                "company_name": "Microsoft Corp.",
                "sec_id": "SEC002",
                "sec_type": "Equity",
                "pos_loc": "US",
                "account": "Main Account",
            },
        ]

    async def get_instrument_terms(self) -> list[dict[str, Any]]:
        """Get instrument terms data. TODO: Replace with DB query."""
        logger.info("Returning mock instrument terms data")
        return [
            {
                "id": 1,
                "deal_num": "D001",
                "detail_id": "DT001",
                "underlying": "AAPL",
                "ticker": "AAPL",
                "company_name": "Apple Inc.",
                "sec_type": "Warrant",
                "effective_date": "2025-01-01",
                "maturity_date": "2027-01-01",
                "first_reset_da": "2025-06-01",
            },
        ]
