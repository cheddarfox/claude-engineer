"""
Time Utilities Module

This module provides utility functions for handling timestamps and time-related operations.
These functions are used throughout the AI Self-Enhancement system for accurate time tracking and analysis.
"""

from datetime import datetime
from error_handling import TimeUtilsError, log_info, log_error

def get_timestamp():
    """
    Get the current timestamp as a formatted string.

    Returns:
        str: Current timestamp in the format 'YYYY-MM-DD HH:MM:SS'.
    """
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_info(f"Generated timestamp: {timestamp}")
        return timestamp
    except Exception as e:
        log_error(f"Error generating timestamp: {str(e)}")
        raise TimeUtilsError("Failed to generate timestamp") from e

def timestamp_to_datetime(timestamp):
    """
    Convert a timestamp string to a datetime object.

    Args:
        timestamp (str): Timestamp string in the format 'YYYY-MM-DD HH:MM:SS'.

    Returns:
        datetime: Datetime object representing the given timestamp.

    Raises:
        TimeUtilsError: If the timestamp is invalid or conversion fails.
    """
    if not isinstance(timestamp, str):
        log_error("Invalid timestamp type")
        raise TimeUtilsError("Timestamp must be a string")

    try:
        dt_object = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        log_info(f"Converted timestamp to datetime: {dt_object}")
        return dt_object
    except ValueError as e:
        log_error(f"Error converting timestamp: {str(e)}")
        raise TimeUtilsError("Invalid timestamp format. Expected 'YYYY-MM-DD HH:MM:SS'") from e

def get_time_difference(start_time, end_time):
    """
    Calculate the time difference between two timestamps.

    Args:
        start_time (str): Start timestamp in the format 'YYYY-MM-DD HH:MM:SS'.
        end_time (str): End timestamp in the format 'YYYY-MM-DD HH:MM:SS'.

    Returns:
        float: Time difference in seconds.

    Raises:
        TimeUtilsError: If the timestamps are invalid or calculation fails.
    """
    try:
        start = timestamp_to_datetime(start_time)
        end = timestamp_to_datetime(end_time)
        difference = (end - start).total_seconds()
        log_info(f"Calculated time difference: {difference} seconds")
        return difference
    except TimeUtilsError:
        raise
    except Exception as e:
        log_error(f"Error calculating time difference: {str(e)}")
        raise TimeUtilsError("Failed to calculate time difference") from e

# Example usage:
# try:
#     current_time = get_timestamp()
#     print(f"Current time: {current_time}")
#
#     start = get_timestamp()
#     # ... some operations ...
#     end = get_timestamp()
#     duration = get_time_difference(start, end)
#     print(f"Operation took {duration} seconds")
# except TimeUtilsError as e:
#     log_error(f"An error occurred in the Time Utils module: {str(e)}")