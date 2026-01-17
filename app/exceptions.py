"""
Portfolio Management Tool - Custom Exceptions

This module re-exports the shared exception hierarchy from pmt_core.
Exceptions are defined in pmt_core for sharing between the Reflex web app
and pmt_core services.

Exception Hierarchy:
    PMTError (base)
    ├── DatabaseConnectionError
    ├── ConfigurationError
    ├── DataExtractionError
    ├── DataValidationError
    ├── ServiceUnavailableError
    └── AuthenticationError
"""

# Re-export all exceptions from pmt_core
from pmt_core.exceptions import (
    PMTError,
    DatabaseConnectionError,
    ConfigurationError,
    DataExtractionError,
    DataValidationError,
    ServiceUnavailableError,
    AuthenticationError,
    # Convenience aliases
    ConnectionError,
    ExtractionError,
    ValidationError,
)

__all__ = [
    "PMTError",
    "DatabaseConnectionError",
    "ConfigurationError",
    "DataExtractionError",
    "DataValidationError",
    "ServiceUnavailableError",
    "AuthenticationError",
    "ConnectionError",
    "ExtractionError",
    "ValidationError",
]
