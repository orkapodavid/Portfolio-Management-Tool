"""
EMSX Service — app-layer wrapper.

Re-exports the core EMSXService from pmt_core_pkg for use
by Reflex state mixins.
"""

from pmt_core.services.emsx import EMSXService

__all__ = ["EMSXService"]
