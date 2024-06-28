"""
Data Persistence Module

This module provides functionality for saving and loading logs and performance data.
It enables the AI system to persist its experiences and learnings over time.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

from error_handling import log_info, log_error, log_debug, DataPersistenceError

# Define the directory where data will be stored
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
DATA_VERSION = "1.0"  # Current version of the data structure

def ensure_data_directory(debug_mode: bool = False) -> None:
    """
    Ensure that the data directory exists.

    Args:
        debug_mode: If True, enables verbose debug logging.

    Raises:
        DataPersistenceError: If unable to create or access the data directory.
    """
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        if debug_mode:
            log_debug(f"Data directory ensured: {DATA_DIR}")
    except Exception as e:
        log_error(f"Error ensuring data directory: {str(e)}")
        raise DataPersistenceError(f"Unable to create or access data directory: {str(e)}")

def is_compatible_version(data: Dict[str, Any]) -> bool:
    """
    Check if the data file version is compatible with the current version.

    Args:
        data: The loaded data to check.

    Returns:
        True if the version is compatible, False otherwise.
    """
    return data.get("version") == DATA_VERSION

def save_logs(logs: List[Dict[str, Any]], debug_mode: bool = False) -> None:
    """
    Save logs to a JSON file.

    Args:
        logs: List of log entries to save.
        debug_mode: If True, enables verbose debug logging.

    Raises:
        DataPersistenceError: If unable to save the logs.
    """
    try:
        ensure_data_directory(debug_mode)
        filename = f"logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(DATA_DIR, filename)
        
        data_to_save = {
            "version": DATA_VERSION,
            "logs": logs
        }
        
        with open(filepath, 'w') as f:
            json.dump(data_to_save, f, indent=2)
        
        log_info(f"Logs saved to {filepath}")
        if debug_mode:
            log_debug(f"Saved {len(logs)} log entries")
    except Exception as e:
        log_error(f"Error saving logs: {str(e)}")
        raise DataPersistenceError(f"Unable to save logs: {str(e)}")

def load_logs(debug_mode: bool = False) -> List[Dict[str, Any]]:
    """
    Load all logs from JSON files in the data directory.

    Args:
        debug_mode: If True, enables verbose debug logging.

    Returns:
        List of all log entries.

    Raises:
        DataPersistenceError: If unable to load the logs.
    """
    try:
        ensure_data_directory(debug_mode)
        logs = []
        
        for filename in os.listdir(DATA_DIR):
            if filename.startswith("logs_") and filename.endswith(".json"):
                filepath = os.path.join(DATA_DIR, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    if is_compatible_version(data):
                        logs.extend(data.get("logs", []))
                    else:
                        log_info(f"Skipping file with incompatible version: {filepath}")
        
        log_info(f"Loaded {len(logs)} log entries")
        if debug_mode:
            log_debug(f"Logs loaded from {len(os.listdir(DATA_DIR))} files")
        return logs
    except Exception as e:
        log_error(f"Error loading logs: {str(e)}")
        raise DataPersistenceError(f"Unable to load logs: {str(e)}")

def save_performance_data(performance_data: Dict[str, Any], debug_mode: bool = False) -> None:
    """
    Save performance data to a JSON file.

    Args:
        performance_data: Performance data to save.
        debug_mode: If True, enables verbose debug logging.

    Raises:
        DataPersistenceError: If unable to save the performance data.
    """
    try:
        ensure_data_directory(debug_mode)
        filename = f"performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(DATA_DIR, filename)
        
        data_to_save = {
            "version": DATA_VERSION,
            "performance_data": performance_data
        }
        
        with open(filepath, 'w') as f:
            json.dump(data_to_save, f, indent=2)
        
        log_info(f"Performance data saved to {filepath}")
        if debug_mode:
            log_debug(f"Saved performance data: {list(performance_data.keys())}")
    except Exception as e:
        log_error(f"Error saving performance data: {str(e)}")
        raise DataPersistenceError(f"Unable to save performance data: {str(e)}")

def load_performance_data(debug_mode: bool = False) -> List[Dict[str, Any]]:
    """
    Load all performance data from JSON files in the data directory.

    Args:
        debug_mode: If True, enables verbose debug logging.

    Returns:
        List of all performance data entries.

    Raises:
        DataPersistenceError: If unable to load the performance data.
    """
    try:
        ensure_data_directory(debug_mode)
        performance_data = []
        
        for filename in os.listdir(DATA_DIR):
            if filename.startswith("performance_") and filename.endswith(".json"):
                filepath = os.path.join(DATA_DIR, filename)
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    if is_compatible_version(data):
                        performance_data.append(data.get("performance_data", {}))
                    else:
                        log_info(f"Skipping file with incompatible version: {filepath}")
        
        log_info(f"Loaded {len(performance_data)} performance data entries")
        if debug_mode:
            log_debug(f"Performance data loaded from {len(os.listdir(DATA_DIR))} files")
        return performance_data
    except Exception as e:
        log_error(f"Error loading performance data: {str(e)}")
        raise DataPersistenceError(f"Unable to load performance data: {str(e)}")

def get_latest_performance_data(debug_mode: bool = False) -> Optional[Dict[str, Any]]:
    """
    Retrieve the latest performance data entry.

    Args:
        debug_mode: If True, enables verbose debug logging.

    Returns:
        The latest performance data entry, or None if no data is available.

    Raises:
        DataPersistenceError: If unable to retrieve the latest performance data.
    """
    try:
        performance_data = load_performance_data(debug_mode)
        if performance_data:
            return performance_data[-1]
        return None
    except Exception as e:
        log_error(f"Error retrieving latest performance data: {str(e)}")
        raise DataPersistenceError(f"Unable to retrieve latest performance data: {str(e)}")

def clean_old_data(days_to_keep: int = 30, debug_mode: bool = False) -> None:
    """
    Clean up old data files to prevent excessive storage usage.

    Args:
        days_to_keep: Number of days of data to keep. Default is 30.
        debug_mode: If True, enables verbose debug logging.

    Raises:
        DataPersistenceError: If unable to clean old data.
    """
    try:
        ensure_data_directory(debug_mode)
        now = datetime.now()
        files_removed = 0
        
        for filename in os.listdir(DATA_DIR):
            if filename.endswith(".json"):
                filepath = os.path.join(DATA_DIR, filename)
                file_date = datetime.fromtimestamp(os.path.getmtime(filepath))
                if (now - file_date).days > days_to_keep:
                    os.remove(filepath)
                    files_removed += 1
        
        log_info(f"Cleaned up {files_removed} old data files")
        if debug_mode:
            log_debug(f"Data cleanup completed. Removed {files_removed} files older than {days_to_keep} days")
    except Exception as e:
        log_error(f"Error cleaning old data: {str(e)}")
        raise DataPersistenceError(f"Unable to clean old data: {str(e)}")

if __name__ == "__main__":
    # Example usage and testing
    debug_mode = True
    
    try:
        # Test saving and loading logs
        test_logs = [{"timestamp": datetime.now().isoformat(), "message": "Test log entry"}]
        save_logs(test_logs, debug_mode)
        loaded_logs = load_logs(debug_mode)
        print(f"Loaded logs: {loaded_logs}")
        
        # Test saving and loading performance data
        test_performance = {"metric1": 0.95, "metric2": 0.87}
        save_performance_data(test_performance, debug_mode)
        loaded_performance = load_performance_data(debug_mode)
        print(f"Loaded performance data: {loaded_performance}")
        
        # Test getting latest performance data
        latest_performance = get_latest_performance_data(debug_mode)
        print(f"Latest performance data: {latest_performance}")
        
        # Test data cleanup
        clean_old_data(days_to_keep=7, debug_mode=debug_mode)
    except DataPersistenceError as e:
        print(f"Data persistence error occurred: {e}")