"""
Operations Service — app-layer wrapper.

Re-exports the core OperationsService from pmt_core_pkg for use
by Reflex state mixins.
"""

from pmt_core.services.operations import OperationsService

__all__ = ["OperationsService"]
