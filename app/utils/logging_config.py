"""
Portfolio Management Tool - Logging Configuration

Provides centralized logging configuration for the application.
Supports environment-based settings and structured logging formats.

Usage:
    from app.utils import logger, get_logger

    # Use default logger
    logger.info("Application started")

    # Get module-specific logger
    my_logger = get_logger("my_module")
    my_logger.debug("Module initialized")
"""

import logging
import os
import sys
from typing import Optional
from datetime import datetime


# =============================================================================
# Logging Configuration
# =============================================================================

DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
STRUCTURED_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s"


def setup_logging(
    level: Optional[str] = None,
    format_string: Optional[str] = None,
    logger_name: str = "pmt",
    log_file: Optional[str] = None,
    structured: bool = False,
) -> logging.Logger:
    """
    Configure logging for the Portfolio Management Tool.

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
               Defaults to LOG_LEVEL environment variable or INFO.
        format_string: Custom log format string. If None, uses default or
                       structured format based on `structured` parameter.
        logger_name: Name of the logger to configure.
        log_file: Optional file path to write logs to.
        structured: If True, uses structured format for log parsing.

    Returns:
        Configured logger instance.

    Example:
        >>> logger = setup_logging(level="DEBUG", structured=True)
        >>> logger.info("Application started")
    """
    # Determine log level
    if level is None:
        level = os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL)

    # Determine format
    if format_string is None:
        format_string = STRUCTURED_FORMAT if structured else DEFAULT_FORMAT

    # Create logger
    app_logger = logging.getLogger(logger_name)
    app_logger.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Clear existing handlers to avoid duplicates
    app_logger.handlers.clear()

    # Create formatter
    formatter = logging.Formatter(format_string, datefmt="%Y-%m-%d %H:%M:%S")

    # Add console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    app_logger.addHandler(console_handler)

    # Add file handler if specified
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)
        app_logger.addHandler(file_handler)

    # Prevent propagation to root logger
    app_logger.propagate = False

    return app_logger


def get_logger(name: str, parent: str = "pmt") -> logging.Logger:
    """
    Get a child logger under the PMT namespace.

    Args:
        name: Logger name (will be prefixed with parent.)
        parent: Parent logger name (default: "pmt")

    Returns:
        Logger instance.

    Example:
        >>> logger = get_logger("services.pnl")
        >>> logger.info("Loading P&L data")
    """
    return logging.getLogger(f"{parent}.{name}")


def log_exception(
    logger: logging.Logger, message: str, exc: Exception, level: int = logging.ERROR
) -> None:
    """
    Log an exception with context.

    Args:
        logger: Logger instance to use.
        message: Context message for the exception.
        exc: The exception to log.
        level: Logging level (default: ERROR).
    """
    logger.log(level, f"{message}: {type(exc).__name__}: {exc}", exc_info=True)


# =============================================================================
# Initialize Default Logger
# =============================================================================

# Create default logger on import
logger = setup_logging()

# Log startup timestamp in debug mode
if os.getenv("LOG_LEVEL", "INFO").upper() == "DEBUG":
    logger.debug(f"Logging initialized at {datetime.now().isoformat()}")


__all__ = ["setup_logging", "get_logger", "log_exception", "logger"]
