"""
Capability Decorator Module

This module provides a decorator for easily defining and registering capabilities
in the AI Self-Enhancement system.
"""

import logging
from functools import wraps

def capability(name, description):
    """
    Decorator for defining a capability.

    Args:
        name (str): The name of the capability.
        description (str): A brief description of what the capability does.

    Returns:
        function: The decorated function.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        wrapper.is_capability = True
        wrapper.capability_name = name
        wrapper.description = description
        return wrapper
    return decorator

class CapabilityValidationError(Exception):
    """Exception raised when a capability fails validation."""
    pass

def validate_capability(func):
    """
    Validate that a function has all required capability attributes.

    Args:
        func (function): The function to validate.

    Raises:
        CapabilityValidationError: If the function is missing required attributes.
    """
    required_attrs = ['is_capability', 'capability_name', 'description']
    for attr in required_attrs:
        if not hasattr(func, attr):
            raise CapabilityValidationError(f"Capability is missing required attribute: {attr}")

def load_capability(func):
    """
    Load a single capability, performing validation and error handling.

    Args:
        func (function): The function to load as a capability.

    Returns:
        dict: A dictionary containing the capability name, description, and function.

    Raises:
        CapabilityValidationError: If the capability fails validation.
    """
    try:
        validate_capability(func)
        return {
            'name': func.capability_name,
            'description': func.description,
            'function': func
        }
    except CapabilityValidationError as e:
        logging.error(f"Failed to load capability {func.__name__}: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Unexpected error loading capability {func.__name__}: {str(e)}")
        return None