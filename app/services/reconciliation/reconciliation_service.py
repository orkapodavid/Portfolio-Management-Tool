"""
Reconciliation Service — app-layer wrapper.

Re-exports the core ReconciliationService from pmt_core_pkg for use
by Reflex state mixins.
"""

from pmt_core.services.reconciliation import ReconciliationService

__all__ = ["ReconciliationService"]
