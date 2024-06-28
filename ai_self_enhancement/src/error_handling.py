"""
Error Handling Module

This module provides custom exception classes and logging setup for the AI Self-Enhancement project.
It enables consistent error handling and logging across all modules.
"""

import logging
from typing import Any
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=f'ai_self_enhancement_log_{datetime.now().strftime("%Y%m%d")}.log',
    filemode='a'
)

logger = logging.getLogger(__name__)

# Custom Exception Classes

class AISelfEnhancementError(Exception):
    """Base exception class for AI Self-Enhancement project."""

    def __init__(self, message: str) -> None:
        """
        Initialize the exception.

        Args:
            message: The error message.
        """
        self.message = message
        logger.error(f"{self.__class__.__name__}: {message}")
        super().__init__(self.message)


class CapabilityError(AISelfEnhancementError):
    """Exception raised for errors in the Capability Registry module."""
    pass


class SelfReflectionError(AISelfEnhancementError):
    """Exception raised for errors in the Self-Reflection module."""
    pass


class TimeUtilsError(AISelfEnhancementError):
    """Exception raised for errors in the Time Utils module."""
    pass


class DataPersistenceError(AISelfEnhancementError):
    """Exception raised for errors in data persistence operations."""
    pass


class ConfigurationError(AISelfEnhancementError):
    """Exception raised for errors in system configuration."""
    pass


# Logging Functions

def log_info(message: str) -> None:
    """
    Log an info message.

    Args:
        message: The message to log.
    """
    logger.info(message)


def log_warning(message: str) -> None:
    """
    Log a warning message.

    Args:
        message: The message to log.
    """
    logger.warning(message)


def log_error(message: str) -> None:
    """
    Log an error message.

    Args:
        message: The message to log.
    """
    logger.error(message)


def log_debug(message: str) -> None:
    """
    Log a debug message.

    Args:
        message: The message to log.
    """
    logger.debug(message)


# Utility Functions

def safe_execute(func: callable, *args: Any, **kwargs: Any) -> Any:
    """
    Safely execute a function and log any errors.

    Args:
        func: The function to execute.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        The result of the function execution.

    Raises:
        AISelfEnhancementError: If an error occurs during execution.
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        log_error(f"Error executing {func.__name__}: {str(e)}")
        raise AISelfEnhancementError(f"Error in {func.__name__}: {str(e)}") from e


if __name__ == "__main__":
    # Example usage
    try:
        # Some operation that might raise an exception
        raise CapabilityError("Failed to add new capability")
    except AISelfEnhancementError as e:
        log_error(f"An error occurred: {str(e)}")

    # Example of using safe_execute
    def example_function(x: int, y: int) -> int:
        return x / y

    result = safe_execute(example_function, 10, 2)
    print(f"Result: {result}")

    try:
        safe_execute(example_function, 10, 0)
    except AISelfEnhancementError as e:
        print(f"Caught error: {e}")