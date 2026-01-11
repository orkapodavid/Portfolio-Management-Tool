import reflex as rx
from app.services import PnLService
from app.states.pnl.types import PnLCurrencyItem


class PnLCurrencyMixin(rx.State, mixin=True):
    """
    Mixin providing P&L Currency data state and filtering.
    """

    # P&L Currency data
    pnl_currency_list: list[PnLCurrencyItem] = []
    is_loading_pnl_currency: bool = False
    pnl_currency_error: str = ""

    # Filters
    pnl_currency_search: str = ""

    async def load_pnl_currency_data(self):
        """Load P&L Currency data from PnLService."""
        self.is_loading_pnl_currency = True
        self.pnl_currency_error = ""
        try:
            service = PnLService()
            self.pnl_currency_list = await service.get_currency_pnl()
        except Exception as e:
            self.pnl_currency_error = str(e)
            import logging

            logging.exception(f"Error loading P&L currency data: {e}")
        finally:
            self.is_loading_pnl_currency = False

    def set_pnl_currency_search(self, query: str):
        self.pnl_currency_search = query

    @rx.var(cache=True)
    def filtered_pnl_currency(self) -> list[PnLCurrencyItem]:
        data = self.pnl_currency_list
        if self.pnl_currency_search:
            query = self.pnl_currency_search.lower()
            data = [item for item in data if query in item.get("currency", "").lower()]
        return data
