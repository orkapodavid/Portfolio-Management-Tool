"""
Market Data Service — app-layer wrapper.

Re-exports the core MarketDataService from pmt_core_pkg for use
by Reflex state mixins.
"""

from pmt_core.services.market_data import MarketDataService

__all__ = ["MarketDataService"]
