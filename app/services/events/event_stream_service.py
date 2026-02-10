"""
Event Stream Service — app-layer wrapper.

Re-exports the core EventStreamService from pmt_core_pkg for use
by Reflex state mixins.
"""

from pmt_core.services.events import EventStreamService

__all__ = ["EventStreamService"]
