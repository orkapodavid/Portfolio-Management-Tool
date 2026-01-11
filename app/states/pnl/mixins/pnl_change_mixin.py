import reflex as rx
from app.services import PnLService
from app.states.pnl.types import PnLChangeItem


class PnLChangeMixin(rx.State, mixin=True):
    """
    Mixin providing P&L Change data state and filtering.
    """

    # P&L Change data
    pnl_change_list: list[PnLChangeItem] = []
    is_loading_pnl_change: bool = False
    pnl_change_error: str = ""

    # Filters
    pnl_change_search: str = ""
    pnl_change_sort_column: str = ""
    pnl_change_sort_direction: str = "asc"

    async def load_pnl_change_data(self):
        """Load P&L Change data from PnLService."""
        self.is_loading_pnl_change = True
        self.pnl_change_error = ""
        try:
            service = PnLService()
            self.pnl_change_list = await service.get_pnl_changes()
        except Exception as e:
            self.pnl_change_error = str(e)
            import logging

            logging.exception(f"Error loading P&L change data: {e}")
        finally:
            self.is_loading_pnl_change = False

    def set_pnl_change_search(self, query: str):
        self.pnl_change_search = query

    def sort_pnl_change(self, column: str):
        if self.pnl_change_sort_column == column:
            self.pnl_change_sort_direction = (
                "desc" if self.pnl_change_sort_direction == "asc" else "asc"
            )
        else:
            self.pnl_change_sort_column = column
            self.pnl_change_sort_direction = "asc"

    @rx.var(cache=True)
    def filtered_pnl_change(self) -> list[PnLChangeItem]:
        data = self.pnl_change_list
        # Filter
        if self.pnl_change_search:
            query = self.pnl_change_search.lower()
            data = [item for item in data if query in item.get("ticker", "").lower()]

        # Sort
        if self.pnl_change_sort_column:

            def get_sort_key(item):
                val = item.get(self.pnl_change_sort_column, "")
                if isinstance(val, str):
                    # Simple heuristic to clean currency/pct for sorting
                    cleaned = (
                        val.replace("$", "")
                        .replace(",", "")
                        .replace("%", "")
                        .replace("(", "-")
                        .replace(")", "")
                    )
                    try:
                        return float(cleaned)
                    except ValueError:
                        return val.lower()
                return val

            data = sorted(
                data,
                key=get_sort_key,
                reverse=(self.pnl_change_sort_direction == "desc"),
            )
        return data
