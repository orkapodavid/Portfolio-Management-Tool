"""
Performance Header Service — app-layer wrapper.

Re-exports the core PerformanceService from pmt_core_pkg as
PerformanceHeaderService for backward compatibility with Reflex states.
"""

from pmt_core.services.performance import PerformanceService as PerformanceHeaderService

__all__ = ["PerformanceHeaderService"]
