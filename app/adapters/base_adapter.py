from app.config import PMT_INTEGRATION_MODE
import logging
import asyncio
from typing import Any, Callable, TypeVar

T = TypeVar("T")


class BaseAdapter:
    """Base adapter class with common utilities and integration mode checking."""

    @staticmethod
    def get_service(service_name: str):
        """Factory method to get the correct service implementation based on mode."""
        if PMT_INTEGRATION_MODE == "mock":
            if service_name == "reporting":
                from app.mocks.pmt_core.services import reporting

                return reporting
            elif service_name == "pricing":
                from app.mocks.pmt_core.services import pricing

                return pricing
            elif service_name == "rules":
                from app.mocks.pmt_core.services import rules

                return rules
        elif PMT_INTEGRATION_MODE == "real":
            raise NotImplementedError("Real integration mode not yet implemented")
        else:
            logging.warning(f"Unknown integration mode: {PMT_INTEGRATION_MODE}")
            return None

    @staticmethod
    async def execute_async(func: Callable[..., T], *args, **kwargs) -> T | None:
        """Helper to execute synchronous core functions in a thread pool."""
        try:
            return await asyncio.to_thread(func, *args, **kwargs)
        except Exception as e:
            logging.exception(f"Error executing service call: {e}")
            return None

    @staticmethod
    def fmt_usd(val: float | None) -> str:
        """Format float as USD string."""
        if val is None:
            return "$0.00"
        return f"${val:,.2f}" if val >= 0 else f"$({abs(val):,.2f})"

    @staticmethod
    def fmt_pct(val: float | None) -> str:
        """Format float as percentage string."""
        if val is None:
            return "0.00%"
        return f"{val:,.2f}%"

    @staticmethod
    def fmt_num(val: float | None) -> str:
        """Format float as number string with parentheses for negative."""
        if val is None:
            return "0.00"
        return f"{val:,.2f}" if val >= 0 else f"({abs(val):,.2f})"

    @staticmethod
    def fmt_bool(val: bool | None) -> str:
        """Format boolean as Yes/No."""
        return "Yes" if val else "No"