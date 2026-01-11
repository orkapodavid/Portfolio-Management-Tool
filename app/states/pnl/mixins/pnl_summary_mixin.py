import reflex as rx
from app.services import PnLService
from app.states.pnl.types import PnLSummaryItem


class PnLSummaryMixin(rx.State, mixin=True):
    """
    Mixin providing P&L Summary data state and filtering.
    """

    # P&L Summary data
    pnl_summary_list: list[PnLSummaryItem] = []
    is_loading_pnl_summary: bool = False
    pnl_summary_error: str = ""

    # Filters
    pnl_summary_search: str = ""
    pnl_summary_sort_column: str = ""
    pnl_summary_sort_direction: str = "asc"

    async def load_pnl_summary_data(self):
        """Load P&L Summary data from PnLService."""
        self.is_loading_pnl_summary = True
        self.pnl_summary_error = ""
        try:
            service = PnLService()
            self.pnl_summary_list = await service.get_pnl_summary()
        except Exception as e:
            self.pnl_summary_error = str(e)
            import logging

            logging.exception(f"Error loading P&L summary data: {e}")
        finally:
            self.is_loading_pnl_summary = False

    def set_pnl_summary_search(self, query: str):
        self.pnl_summary_search = query

    def sort_pnl_summary(self, column: str):
        if self.pnl_summary_sort_column == column:
            self.pnl_summary_sort_direction = (
                "desc" if self.pnl_summary_sort_direction == "asc" else "asc"
            )
        else:
            self.pnl_summary_sort_column = column
            self.pnl_summary_sort_direction = "asc"

    @rx.var(cache=True)
    def filtered_pnl_summary(self) -> list[PnLSummaryItem]:
        data = self.pnl_summary_list
        if self.pnl_summary_search:
            query = self.pnl_summary_search.lower()
            data = [
                item for item in data if query in item.get("underlying", "").lower()
            ]

        # Add sorting logic similar to others if needed
        # For now just returning filtered
        return data
