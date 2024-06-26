"""
Data Persistence Module

This module provides functionality for saving and loading logs and performance data.
It enables the AI system to persist its experiences and learnings over time.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any

# Define the directory where data will be stored
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

def ensure_data_directory():
    """Ensure that the data directory exists."""
    os.makedirs(DATA_DIR, exist_ok=True)

def save_logs(logs: List[Dict[str, Any]]):
    """
    Save logs to a JSON file.

    Args:
        logs (List[Dict[str, Any]]): List of log entries to save.
    """
    ensure_data_directory()
    filename = f"logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(DATA_DIR, filename)
    
    with open(filepath, 'w') as f:
        json.dump(logs, f, indent=2)

def load_logs() -> List[Dict[str, Any]]:
    """
    Load all logs from JSON files in the data directory.

    Returns:
        List[Dict[str, Any]]: List of all log entries.
    """
    ensure_data_directory()
    logs = []
    
    for filename in os.listdir(DATA_DIR):
        if filename.startswith("logs_") and filename.endswith(".json"):
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, 'r') as f:
                logs.extend(json.load(f))
    
    return logs

def save_performance_data(performance_data: Dict[str, Any]):
    """
    Save performance data to a JSON file.

    Args:
        performance_data (Dict[str, Any]): Performance data to save.
    """
    ensure_data_directory()
    filename = f"performance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = os.path.join(DATA_DIR, filename)
    
    with open(filepath, 'w') as f:
        json.dump(performance_data, f, indent=2)

def load_performance_data() -> List[Dict[str, Any]]:
    """
    Load all performance data from JSON files in the data directory.

    Returns:
        List[Dict[str, Any]]: List of all performance data entries.
    """
    ensure_data_directory()
    performance_data = []
    
    for filename in os.listdir(DATA_DIR):
        if filename.startswith("performance_") and filename.endswith(".json"):
            filepath = os.path.join(DATA_DIR, filename)
            with open(filepath, 'r') as f:
                performance_data.append(json.load(f))
    
    return performance_data