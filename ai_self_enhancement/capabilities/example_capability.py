"""
Example Custom Capability

This module demonstrates how to create a custom capability using the
capability decorator.
"""

from src.capability_decorator import capability

@capability(name="reverse_string", description="Reverses the input string")
def reverse_string(text):
    """
    Reverse the input string.

    Args:
        text (str): The input string to reverse.

    Returns:
        str: The reversed string.
    """
    return text[::-1]

@capability(name="count_words", description="Counts the number of words in the input string")
def count_words(text):
    """
    Count the number of words in the input string.

    Args:
        text (str): The input string to count words from.

    Returns:
        int: The number of words in the input string.
    """
    return len(text.split())

# This function will not be loaded as a capability because it doesn't use the decorator
def helper_function():
    """A helper function that should not be loaded as a capability."""
    pass