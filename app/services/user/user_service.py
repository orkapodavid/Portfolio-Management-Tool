"""
User Service — app-layer wrapper.

Re-exports the core UserService from pmt_core_pkg for use
by Reflex state mixins.
"""

from pmt_core.services.user import UserService

__all__ = ["UserService"]
