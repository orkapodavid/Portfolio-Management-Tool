"""
Compliance Service - Handles compliance and regulatory data.

Uses pmt_core.ComplianceRecord and ComplianceType for type-safe data contracts.
TODO: Replace with real database queries for production.
"""

import logging
import random
from datetime import datetime, timedelta

from pmt_core import ComplianceRecord, ComplianceType

logger = logging.getLogger(__name__)


class ComplianceService:
    """Service for compliance and regulatory data retrieval."""

    async def get_restricted_list(self) -> list[ComplianceRecord]:
        """Get restricted securities list."""
        logger.warning("Using mock restricted list data.")

        tickers = ["AAPL", "TSLA", "NVDA", "META", "GOOGL", "AMZN", "MSFT"]

        return [
            ComplianceRecord(
                id=i,
                ticker=ticker,
                company_name=f"{ticker} Inc.",
                compliance_type=ComplianceType.RESTRICTED.value,
                in_emsx="Yes" if random.random() > 0.3 else "No",
                firm_block="Yes" if random.random() > 0.7 else "No",
                compliance_start=(
                    datetime.now() - timedelta(days=random.randint(1, 90))
                ).strftime("%Y-%m-%d"),
                nda_end=(
                    datetime.now() + timedelta(days=random.randint(30, 180))
                ).strftime("%Y-%m-%d"),
                mnpi_end=(
                    datetime.now() + timedelta(days=random.randint(30, 180))
                ).strftime("%Y-%m-%d"),
                wc_end=(
                    datetime.now() + timedelta(days=random.randint(30, 180))
                ).strftime("%Y-%m-%d"),
                undertaking_expiry=None,
                account=None,
                undertaking_type=None,
                undertaking_details=None,
            )
            for i, ticker in enumerate(tickers * 2)
        ]

    async def get_undertakings(self) -> list[ComplianceRecord]:
        """Get undertakings data."""
        logger.warning("Using mock undertakings data.")

        tickers = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA"]
        undertaking_types = ["Lock-up", "Standstill", "Non-compete", "ROFR"]

        return [
            ComplianceRecord(
                id=i,
                ticker=ticker,
                company_name=f"{ticker} Inc.",
                compliance_type=ComplianceType.UNDERTAKING.value,
                in_emsx=None,
                firm_block=None,
                compliance_start=None,
                nda_end=None,
                mnpi_end=None,
                wc_end=None,
                undertaking_expiry=(
                    datetime.now() + timedelta(days=random.randint(30, 365))
                ).strftime("%Y-%m-%d"),
                account=f"ACC{random.randint(100, 999)}",
                undertaking_type=random.choice(undertaking_types),
                undertaking_details=f"Standard {random.choice(undertaking_types)} agreement",
            )
            for i, ticker in enumerate(tickers * 2)
        ]

    async def get_beneficial_ownership(self) -> list[ComplianceRecord]:
        """Get beneficial ownership data."""
        logger.warning("Using mock beneficial ownership data.")

        tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"]

        return [
            ComplianceRecord(
                id=i,
                ticker=ticker,
                company_name=f"{ticker} Inc.",
                compliance_type=ComplianceType.BENEFICIAL_OWNERSHIP.value,
                in_emsx=None,
                firm_block=None,
                compliance_start=(datetime.now() - timedelta(days=i)).strftime(
                    "%Y-%m-%d"
                ),
                nda_end=None,
                mnpi_end=None,
                wc_end=None,
                undertaking_expiry=None,
                account=None,
                undertaking_type=None,
                undertaking_details=None,
            )
            for i, ticker in enumerate(tickers * 2)
        ]

    async def get_monthly_exercise_limit(self) -> list[dict]:
        """Get monthly exercise limit data."""
        logger.warning("Using mock monthly exercise limit data.")

        tickers = ["AAPL", "MSFT", "GOOGL"]
        sec_types = ["Warrant", "Option", "Convertible"]

        return [
            {
                "id": i,
                "underlying": f"{ticker} US Equity",
                "ticker": ticker,
                "company_name": f"{ticker} Inc.",
                "sec_type": random.choice(sec_types),
                "original_nosh": f"{random.randint(100, 500):,}M",
                "original_quantity": f"{random.randint(10, 50):,}M",
                "monthly_exercised_quantity": f"{random.randint(1, 10):,}M",
                "monthly_exercised_pct": f"{random.uniform(1, 10):.2f}%",
                "monthly_sal": f"{random.uniform(5, 20):.2f}%",
            }
            for i, ticker in enumerate(tickers * 3)
        ]
