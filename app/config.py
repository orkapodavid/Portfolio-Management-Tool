import os
from enum import Enum


class IntegrationMode(Enum):
    """Modes for integrating with the business logic core.

    This enum defines how the Reflex application retrieves its data.
    It is controlled by the `PMT_INTEGRATION_MODE` environment variable.
    """

    MOCK = "mock"
    """
    Use internal mock services located in `app/mocks/pmt_core`.
    This is the default mode for frontend development when the backend is not available.
    It simulates API delays and returns static sample data.
    """
    REAL = "real"
    """
    Use the actual `pmt_core` package.
    Requires `pmt_core` to be installed in the Python environment.
    Connects to real database and Bloomberg services via `pmt_core`.
    """
    STANDALONE = "standalone"
    """
    Legacy mode using direct internal implementations (e.g., yfinance).
    Used for features that haven't been migrated to `pmt_core` yet.
    """


PMT_INTEGRATION_MODE = os.getenv("PMT_INTEGRATION_MODE", "mock")
PMT_CORE_PATH = os.getenv("PMT_CORE_PATH", None)