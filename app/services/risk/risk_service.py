"""
Risk Service — app-layer wrapper.

Re-exports the core RiskService from pmt_core_pkg for use
by Reflex state mixins.
"""

from pmt_core.services.risk import RiskService

__all__ = ["RiskService"]
