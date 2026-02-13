"""
Reference Data Mixin — State mixin for the Market Data Reference Data tab.

Loads reference data from ReferenceDataService.
"""

import reflex as rx
from starter_app.services import ReferenceDataService

_reference_service = ReferenceDataService()


class ReferenceDataMixin(rx.State, mixin=True):
    """Mixin providing Market Data Reference Data state."""

    # AG Grid state
    ref_row_data: list[dict] = []
    is_loading_ref: bool = False
    ref_error: str = ""

    # Search
    ref_search_text: str = ""

    @rx.event
    def load_reference_data(self):
        """Load reference data from ReferenceDataService."""
        self.is_loading_ref = True
        self.ref_error = ""
        try:
            self.ref_row_data = _reference_service.get_reference_data()
        except Exception as e:
            self.ref_error = str(e)
        finally:
            self.is_loading_ref = False

    @rx.event
    def set_ref_search(self, value: str):
        self.ref_search_text = value

    @rx.event
    def clear_ref_search(self):
        self.ref_search_text = ""

    @rx.var(cache=True)
    def ref_row_count(self) -> int:
        """Total number of reference data rows."""
        return len(self.ref_row_data)
