import reflex as rx
from app.services import PositionService
from app.states.positions.types import TradeSummaryItem


class TradeSummaryMixin(rx.State, mixin=True):
    """
    Mixin providing Trade Summary data state.
    """

    trade_summaries: list[TradeSummaryItem] = []
    is_loading_trade_summaries: bool = False
    trade_summary_error: str = ""

    trade_summary_search: str = ""

    async def load_trade_summary_data(self):
        """Load trade summary data."""
        self.is_loading_trade_summaries = True
        self.trade_summary_error = ""
        try:
            service = PositionService()
            self.trade_summaries = await service.get_trade_summary()
        except Exception as e:
            self.trade_summary_error = str(e)
            import logging

            logging.exception(f"Error loading trade summary: {e}")
        finally:
            self.is_loading_trade_summaries = False

    def set_trade_summary_search(self, query: str):
        self.trade_summary_search = query

    @rx.var(cache=True)
    def filtered_trade_summaries(self) -> list[TradeSummaryItem]:
        data = self.trade_summaries
        if self.trade_summary_search:
            query = self.trade_summary_search.lower()
            data = [item for item in data if query in item.get("ticker", "").lower()]
        return data
