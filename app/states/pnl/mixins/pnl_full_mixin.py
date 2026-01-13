import reflex as rx
from app.services import PnLService
from app.states.pnl.types import PnLFullItem


class PnLFullMixin(rx.State, mixin=True):
    """
    Mixin providing P&L Full data state and filtering.
    """

    # P&L Full data
    pnl_full_list: list[PnLFullItem] = []
    is_loading_pnl_full: bool = False
    pnl_full_error: str = ""

    # Filters
    pnl_full_search: str = ""

    async def load_pnl_full_data(self):
        """Load P&L Full data from PnLService."""
        self.is_loading_pnl_full = True
        self.pnl_full_error = ""
        try:
            service = PnLService()
            self.pnl_full_list = await service.get_pnl_full()
        except Exception as e:
            self.pnl_full_error = str(e)
            import logging

            logging.exception(f"Error loading P&L full data: {e}")
        finally:
            self.is_loading_pnl_full = False

    def set_pnl_full_search(self, query: str):
        self.pnl_full_search = query

    @rx.var(cache=True)
    def filtered_pnl_full(self) -> list[PnLFullItem]:
        data = self.pnl_full_list
        if self.pnl_full_search:
            query = self.pnl_full_search.lower()
            data = [
                item
                for item in data
                if query in item.get("ticker", "").lower()
                or query in item.get("underlying", "").lower()
            ]
        return data
