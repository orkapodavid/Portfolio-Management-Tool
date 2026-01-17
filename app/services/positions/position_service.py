"""
Position Service for Portfolio Management Tool.

This service handles position data fetching and processing.
Uses pmt_core.PositionRecord and InstrumentType for type-safe data contracts.

TODO: Implement using source/reports/position_tab/ business logic.
"""

import asyncio
import logging
from typing import Optional
from datetime import datetime

from app.services.shared.database_service import DatabaseService
from pmt_core import PositionRecord, InstrumentType
from pmt_core.models.enums import Currency

logger = logging.getLogger(__name__)


class PositionService:
    """
    Service for fetching and processing position data.

    This can integrate with the PyQt app's position extraction logic from:
    - source/reports/position_tab/position_full/
    - source/reports/position_tab/position_eod_*/
    """

    def __init__(self, db_service: Optional[DatabaseService] = None):
        """
        Initialize position service.

        Args:
            db_service: Optional database service
        """
        self.db = db_service or DatabaseService()

    async def get_positions(
        self, position_date: Optional[str] = None, account_id: Optional[str] = None
    ) -> list[PositionRecord]:
        """
        Get all positions for a given date.

        Args:
            position_date: Position date (YYYY-MM-DD), defaults to today
            account_id: Optional account filter

        Returns:
            List of PositionRecord dictionaries
        """
        logger.warning("Using mock position data. Implement real DB/PyQt integration!")

        # Mock data
        if not position_date:
            position_date = datetime.now().strftime("%Y-%m-%d")

        tickers = [
            "TKR0",
            "TKR1",
            "TKR2",
            "TKR3",
            "TKR4",
            "TKR5",
            "TKR6",
            "TKR7",
            "TKR8",
            "TKR9",
        ]
        locations = ["NY", "HK", "LN"]
        currencies = [Currency.USD.value, Currency.HKD.value, Currency.GBP.value]

        return [
            PositionRecord(
                id=i,
                trade_date=position_date,
                deal_num=f"DEAL{i:03d}",
                detail_id=f"D{i:03d}",
                underlying=f"{tickers[i]} US Equity",
                ticker=tickers[i],
                company_name=f"Company {i}",
                sec_id=f"SEC{i:06d}",
                sec_type=InstrumentType.STOCK.value,
                subtype=None,
                currency=currencies[i % len(currencies)],
                account_id="ACC001",
                pos_loc=locations[i % len(locations)],
                notional=f"${(i + 1) * 50000:,.2f}",
                position=f"{(i + 1) * 1000}",
                market_value=f"${(i + 1) * 52500:,.2f}",
            )
            for i in range(10)
        ]

    async def get_stock_positions(
        self, position_date: Optional[str] = None
    ) -> list[PositionRecord]:
        """
        Get stock positions only.

        Returns positions filtered by sec_type = InstrumentType.STOCK
        """
        logger.info("Returning mock stock position data")
        if not position_date:
            position_date = datetime.now().strftime("%Y-%m-%d")

        tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META", "TSLA", "AMD"]
        currencies = [Currency.USD.value, Currency.EUR.value, Currency.GBP.value]
        locations = ["NY", "HK", "LN"]

        return [
            PositionRecord(
                id=i + 1,
                trade_date=position_date,
                deal_num=f"DEAL{i + 1:03d}",
                detail_id=f"STK{i + 1:03d}",
                underlying=f"{tickers[i % len(tickers)]} US Equity",
                ticker=tickers[i % len(tickers)],
                company_name=f"{tickers[i % len(tickers)]} Inc.",
                sec_id=f"SEC{i + 1:06d}",
                sec_type=InstrumentType.STOCK.value,
                subtype=None,
                currency=currencies[i % len(currencies)],
                account_id=f"ACC{(i % 3) + 1:03d}",
                pos_loc=locations[i % len(locations)],
                notional=f"${(i + 1) * 50000:,.2f}",
                position=f"{(i + 1) * 500}",
                market_value=f"${(i + 1) * 52500:,.2f}",
            )
            for i in range(15)
        ]

    async def get_warrant_positions(
        self, position_date: Optional[str] = None
    ) -> list[PositionRecord]:
        """
        Get warrant positions only.

        Returns positions filtered by sec_type = InstrumentType.WARRANT
        """
        logger.info("Returning mock warrant position data")
        if not position_date:
            position_date = datetime.now().strftime("%Y-%m-%d")

        underlyings = ["AAPL", "TSLA", "NVDA", "AMD", "META"]
        currencies = [Currency.USD.value, Currency.EUR.value]

        return [
            PositionRecord(
                id=i + 1,
                trade_date=position_date,
                deal_num=f"WDEAL{i + 1:03d}",
                detail_id=f"WAR{i + 1:03d}",
                underlying=underlyings[i % len(underlyings)],
                ticker=f"{underlyings[i % len(underlyings)]}-W{i + 1}",
                company_name=f"{underlyings[i % len(underlyings)]} Inc.",
                sec_id=f"WSEC{i + 1:06d}",
                sec_type=InstrumentType.WARRANT.value,
                subtype=["Call", "Put"][i % 2],
                currency=currencies[i % len(currencies)],
                account_id=f"ACC{(i % 3) + 1:03d}",
                pos_loc="NY",
                notional=f"${(i + 1) * 25000:,.2f}",
                position=f"{(i + 1) * 1000}",
                market_value=f"${(i + 1) * 27500:,.2f}",
            )
            for i in range(10)
        ]

    async def get_bond_positions(
        self, position_date: Optional[str] = None
    ) -> list[PositionRecord]:
        """
        Get bond positions only.

        Returns positions filtered by sec_type = InstrumentType.BOND or CONVERTIBLE
        """
        logger.info("Returning mock bond position data")
        if not position_date:
            position_date = datetime.now().strftime("%Y-%m-%d")

        issuers = ["AAPL", "MSFT", "GOOGL", "AMZN", "JPM", "BAC"]
        currencies = [Currency.USD.value, Currency.EUR.value, Currency.GBP.value]

        return [
            PositionRecord(
                id=i + 1,
                trade_date=position_date,
                deal_num=f"BDEAL{i + 1:03d}",
                detail_id=f"BND{i + 1:03d}",
                underlying=issuers[i % len(issuers)],
                ticker=f"{issuers[i % len(issuers)]}-CB{i + 1}",
                company_name=f"{issuers[i % len(issuers)]} Inc.",
                sec_id=f"BSEC{i + 1:06d}",
                sec_type=InstrumentType.CONVERTIBLE.value,
                subtype=["Senior", "Junior", "Subordinated"][i % 3],
                currency=currencies[i % len(currencies)],
                account_id=f"ACC{(i % 3) + 1:03d}",
                pos_loc="NY",
                notional=f"${(i + 1) * 100000:,.2f}",
                position=f"{(i + 1) * 100}",
                market_value=f"${(i + 1) * 105000:,.2f}",
            )
            for i in range(8)
        ]

    async def get_trade_summary(
        self, start_date: Optional[str] = None, end_date: Optional[str] = None
    ) -> list[PositionRecord]:
        """
        Get trade summary for date range.

        TODO: Replace with DB query for trade summary data.
        """
        logger.info("Returning mock trade summary data")
        if not start_date:
            start_date = datetime.now().strftime("%Y-%m-%d")

        tickers = ["AAPL", "TSLA", "NVDA", "META", "MSFT", "AMD"]
        sec_types = [InstrumentType.WARRANT.value, InstrumentType.CONVERTIBLE.value]
        currencies = [Currency.USD.value, Currency.EUR.value, Currency.GBP.value]

        return [
            PositionRecord(
                id=i + 1,
                trade_date=start_date,
                deal_num=f"TDEAL{i + 1:03d}",
                detail_id=f"TS{i + 1:03d}",
                underlying=tickers[i % len(tickers)],
                ticker=tickers[i % len(tickers)],
                company_name=f"{tickers[i % len(tickers)]} Inc.",
                sec_id=f"TSEC{i + 1:06d}",
                sec_type=sec_types[i % len(sec_types)],
                subtype=["Call", "Put", "Senior", "Junior"][i % 4],
                currency=currencies[i % len(currencies)],
                account_id=f"ACC{(i % 3) + 1:03d}",
                pos_loc="NY",
                notional=f"${(i + 1) * 75000:,.2f}",
                position=f"{(i + 1) * 200}",
                market_value=f"${(i + 1) * 80000:,.2f}",
            )
            for i in range(12)
        ]


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    async def test_position_service():
        service = PositionService()

        # Test get_positions
        positions = await service.get_positions()
        print(f"Positions count: {len(positions)}")
        if positions:
            print(f"Sample position: {positions[0]}")

    asyncio.run(test_position_service())
