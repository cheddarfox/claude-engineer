"""
Error Handling Module

This module provides custom exception classes and logging setup for the AI Self-Enhancement project.
It enables consistent error handling and logging across all modules.
"""

import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename=f'ai_self_enhancement_log_{datetime.now().strftime("%Y%m%d")}.log',
    filemode='a'
)

logger = logging.getLogger(__name__)

class AISelfEnhancementError(Exception):
    """Base exception class for AI Self-Enhancement project."""
    def __init__(self, message):
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

def log_info(message):
    """Log an info message."""
    logger.info(message)

def log_warning(message):
    """Log a warning message."""
    logger.warning(message)

def log_error(message):
    """Log an error message."""
    logger.error(message)

# Example usage:
# try:
#     # Some operation that might raise an exception
#     raise CapabilityError("Failed to add new capability")
# except AISelfEnhancementError as e:
#     log_error(f"An error occurred: {str(e)}")