"""
Reverse Inquiry Service — app-layer wrapper.

Re-exports the core ReverseInquiryService from pmt_core_pkg for use
by Reflex state mixins.
"""

from pmt_core.services.events import ReverseInquiryService

__all__ = ["ReverseInquiryService"]
