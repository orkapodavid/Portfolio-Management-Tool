"""
PnL Service — app-layer wrapper.

Re-exports the core PnLService from pmt_core_pkg for use
by Reflex state mixins.
"""

from pmt_core.services.pnl import PnLService

__all__ = ["PnLService"]
