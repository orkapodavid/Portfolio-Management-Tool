"""
Instruments Service — app-layer wrapper.

Re-exports the core InstrumentsService from pmt_core_pkg for use
by Reflex state mixins.
"""

from pmt_core.services.instruments import InstrumentsService

__all__ = ["InstrumentsService"]
