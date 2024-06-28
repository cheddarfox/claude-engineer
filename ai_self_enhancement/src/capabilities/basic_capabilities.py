"""
Basic Capabilities Module

This module contains example capabilities that can be dynamically loaded by the AI system.
These functions demonstrate how capabilities can be implemented and used within the system.
"""

def greet(name: str) -> str:
    """
    A simple greeting capability.

    Args:
        name (str): The name of the person to greet.

    Returns:
        str: A greeting message.
    """
    return f"Hello, {name}! I'm an AI with dynamically loaded capabilities."

def calculate_sum(*args: float) -> float:
    """
    Calculate the sum of given numbers.

    Args:
        *args (float): Any number of numeric values.

    Returns:
        float: The sum of all provided numbers.
    """
    return sum(args)

def reverse_string(text: str) -> str:
    """
    Reverse a given string.

    Args:
        text (str): The string to reverse.

    Returns:
        str: The reversed string.
    """
    return text[::-1]

def count_words(text: str) -> int:
    """
    Count the number of words in a given text.

    Args:
        text (str): The text to analyze.

    Returns:
        int: The number of words in the text.
    """
    return len(text.split())

# You can add more capability functions here as needed