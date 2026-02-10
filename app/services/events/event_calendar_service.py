"""
Event Calendar Service — app-layer wrapper.

Re-exports the core EventCalendarService from pmt_core_pkg for use
by Reflex state mixins.
"""

from pmt_core.services.events import EventCalendarService

__all__ = ["EventCalendarService"]
