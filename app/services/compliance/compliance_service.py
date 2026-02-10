"""
Compliance Service — app-layer wrapper.

Re-exports the core ComplianceService from pmt_core_pkg for use
by Reflex state mixins.
"""

from pmt_core.services.compliance import ComplianceService

__all__ = ["ComplianceService"]
