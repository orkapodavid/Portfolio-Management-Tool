"""
Stock Screener Mixin - Tab-specific state for Stock Screener data.

Provides auto-refresh background task, force refresh, and row-level
filter state for DTL10, Market Cap, $ADV 3M (range), and Country (multiselect).
"""

import asyncio
from datetime import datetime

import reflex as rx
from app.states.instruments.types import StockScreenerItem
import logging
import random
from app.services import services

class StockScreenerMixin(rx.State, mixin=True):
    """
    Mixin providing Stock Screener data state with auto-refresh
    and row-level filters.
    """

    # Stock Screener data
    stock_screener: list[StockScreenerItem] = []
    is_loading_stock_screener: bool = False
    stock_screener_last_updated: str = "—"
    stock_screener_auto_refresh: bool = True

    # =====================================================================
    # ROW-LEVEL FILTERS
    # =====================================================================

    # DTL10 range filter (numeric)
    screener_dtl10_min: str = ""
    screener_dtl10_max: str = ""

    # Market Cap (MM USD) range filter (numeric)
    screener_mkt_cap_min: str = ""
    screener_mkt_cap_max: str = ""

    # $ADV 3M range filter (numeric)
    screener_adv_3m_min: str = ""
    screener_adv_3m_max: str = ""

    # Country multiselect filter
    screener_selected_countries: list[str] = []

    # Track active filters for the Clear button
    screener_filters_active: bool = False

    # =====================================================================
    # FILTER HANDLERS
    # =====================================================================

    def set_screener_dtl10_min(self, v: str):
        self.screener_dtl10_min = v

    def set_screener_dtl10_max(self, v: str):
        self.screener_dtl10_max = v

    def set_screener_mkt_cap_min(self, v: str):
        self.screener_mkt_cap_min = v

    def set_screener_mkt_cap_max(self, v: str):
        self.screener_mkt_cap_max = v

    def set_screener_adv_3m_min(self, v: str):
        self.screener_adv_3m_min = v

    def set_screener_adv_3m_max(self, v: str):
        self.screener_adv_3m_max = v

    def toggle_screener_country(self, country: str):
        """Toggle a country in the multiselect list."""
        if country in self.screener_selected_countries:
            self.screener_selected_countries = [
                c for c in self.screener_selected_countries if c != country
            ]
        else:
            self.screener_selected_countries = [
                *self.screener_selected_countries,
                country,
            ]

    def apply_screener_filters(self):
        """Mark filters as active (the filtered_stock_screener var does actual filtering)."""
        has_any = bool(
            self.screener_dtl10_min
            or self.screener_dtl10_max
            or self.screener_mkt_cap_min
            or self.screener_mkt_cap_max
            or self.screener_adv_3m_min
            or self.screener_adv_3m_max
            or self.screener_selected_countries
        )
        self.screener_filters_active = has_any

    def clear_screener_filters(self):
        """Reset all filter state."""
        self.screener_dtl10_min = ""
        self.screener_dtl10_max = ""
        self.screener_mkt_cap_min = ""
        self.screener_mkt_cap_max = ""
        self.screener_adv_3m_min = ""
        self.screener_adv_3m_max = ""
        self.screener_selected_countries = []
        self.screener_filters_active = False

    def handle_screener_filter_key(self, key: str):
        """Handle key press in filter inputs — Enter triggers Apply."""
        if key == "Enter":
            self.apply_screener_filters()

    # =====================================================================
    # AVAILABLE COUNTRIES (derived from data)
    # =====================================================================

    @rx.var(cache=True)
    def screener_available_countries(self) -> list[str]:
        """Unique country values from the loaded data."""
        countries = sorted(
            {item.get("country", "") for item in self.stock_screener if item.get("country")}
        )
        return countries

    # =====================================================================
    # FILTERED DATA
    # =====================================================================

    @rx.var(cache=True)
    def filtered_stock_screener(self) -> list[StockScreenerItem]:
        """Apply row-level filters when active."""
        data = self.stock_screener

        if not self.screener_filters_active:
            return data

        result = []
        for item in data:
            # DTL10 range
            if self.screener_dtl10_min or self.screener_dtl10_max:
                try:
                    val = float(str(item.get("dtl10", "0")).replace(",", ""))
                    if self.screener_dtl10_min and val < float(self.screener_dtl10_min):
                        continue
                    if self.screener_dtl10_max and val > float(self.screener_dtl10_max):
                        continue
                except (ValueError, TypeError):
                    continue

            # Market Cap (MM USD) range
            if self.screener_mkt_cap_min or self.screener_mkt_cap_max:
                try:
                    val = float(str(item.get("mkt_cap_usd", "0")).replace(",", ""))
                    if self.screener_mkt_cap_min and val < float(self.screener_mkt_cap_min):
                        continue
                    if self.screener_mkt_cap_max and val > float(self.screener_mkt_cap_max):
                        continue
                except (ValueError, TypeError):
                    continue

            # $ADV 3M range
            if self.screener_adv_3m_min or self.screener_adv_3m_max:
                try:
                    val = float(str(item.get("adv_3m_usd", "0")).replace(",", ""))
                    if self.screener_adv_3m_min and val < float(self.screener_adv_3m_min):
                        continue
                    if self.screener_adv_3m_max and val > float(self.screener_adv_3m_max):
                        continue
                except (ValueError, TypeError):
                    continue

            # Country multiselect
            if self.screener_selected_countries:
                if item.get("country", "") not in self.screener_selected_countries:
                    continue

            result.append(item)

        return result

    # =====================================================================
    # DATA LOADING
    # =====================================================================

    async def load_stock_screener_data(self):
        """Load Stock Screener data from InstrumentsService."""
        self.is_loading_stock_screener = True
        try:
            self.stock_screener = await services.instruments.get_stock_screener()
            self.stock_screener_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error loading stock screener data: {e}")
        finally:
            self.is_loading_stock_screener = False

    @rx.event(background=True)
    async def start_stock_screener_auto_refresh(self):
        """Background task for Stock Screener auto-refresh (2s interval)."""
        while True:
            async with self:
                if not self.stock_screener_auto_refresh:
                    break
                self.simulate_stock_screener_update()
            await asyncio.sleep(2)

    def toggle_stock_screener_auto_refresh(self, value: bool):
        """Toggle auto-refresh state. Restarts background task if enabled."""
        self.stock_screener_auto_refresh = value
        if value:
            return type(self).start_stock_screener_auto_refresh

    def simulate_stock_screener_update(self):
        """Simulated delta update for demo - random price/cap changes."""
        if not self.stock_screener_auto_refresh or len(self.stock_screener) < 1:
            return

        new_list = list(self.stock_screener)

        for _ in range(random.randint(1, min(3, len(new_list)))):
            idx = random.randint(0, len(new_list) - 1)
            old_row = new_list[idx]
            new_row = dict(old_row)

            # Simulate last_price changes
            if "last_price" in new_row and new_row["last_price"]:
                try:
                    val = float(str(new_row["last_price"]).replace(",", ""))
                    new_val = round(val * random.uniform(0.995, 1.005), 2)
                    new_row["last_price"] = f"{new_val:,.2f}"
                except (ValueError, TypeError):
                    pass

            # Simulate mkt_cap_usd changes
            if "mkt_cap_usd" in new_row and new_row["mkt_cap_usd"]:
                try:
                    val = float(str(new_row["mkt_cap_usd"]).replace(",", ""))
                    new_val = round(val * random.uniform(0.99, 1.01), 2)
                    new_row["mkt_cap_usd"] = f"{new_val:,.2f}"
                except (ValueError, TypeError):
                    pass

            new_list[idx] = new_row

        self.stock_screener = new_list
        self.stock_screener_last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    async def force_refresh_stock_screener(self):
        """Force refresh stock screener data with loading overlay."""
        if self.is_loading_stock_screener:
            return
        self.is_loading_stock_screener = True
        yield
        await asyncio.sleep(0.3)
        try:
            self.stock_screener = await services.instruments.get_stock_screener()
            self.stock_screener_last_updated = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        except Exception as e:

            logging.exception(f"Error refreshing stock screener: {e}")
        finally:
            self.is_loading_stock_screener = False
