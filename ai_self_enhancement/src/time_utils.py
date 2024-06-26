"""
Time Utilities Module

This module provides utility functions for handling timestamps and time-related operations.
These functions are used throughout the AI Self-Enhancement system for accurate time tracking and analysis.
"""

from datetime import datetime

def get_timestamp():
    """
    Get the current timestamp as a formatted string.

    Returns:
        str: Current timestamp in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def timestamp_to_datetime(timestamp):
    """
    Convert a timestamp string to a datetime object.

    Args:
        timestamp (str): Timestamp string in the format 'YYYY-MM-DD HH:MM:SS'.

    Returns:
        datetime: Datetime object representing the given timestamp.
    """
    return datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

def get_time_difference(start_time, end_time):
    """
    Calculate the time difference between two timestamps.

    Args:
        start_time (str): Start timestamp in the format 'YYYY-MM-DD HH:MM:SS'.
        end_time (str): End timestamp in the format 'YYYY-MM-DD HH:MM:SS'.

    Returns:
        float: Time difference in seconds.
    """
    start = timestamp_to_datetime(start_time)
    end = timestamp_to_datetime(end_time)
    return (end - start).total_seconds()

# Example usage:
# current_time = get_timestamp()
# print(f"Current time: {current_time}")
#
# start = get_timestamp()
# # ... some operations ...
# end = get_timestamp()
# duration = get_time_difference(start, end)
# print(f"Operation took {duration} seconds")