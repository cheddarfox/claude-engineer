import pytest
import os
import json
from datetime import datetime, timedelta
from ai_self_enhancement.src.data_persistence import (
    ensure_data_directory,
    save_logs,
    load_logs,
    save_performance_data,
    load_performance_data,
    clean_old_data,
    DATA_DIR
)
from ai_self_enhancement.src.error_handling import log_debug

@pytest.fixture
def cleanup_data_dir():
    yield
    for file in os.listdir(DATA_DIR):
        os.remove(os.path.join(DATA_DIR, file))

def test_ensure_data_directory():
    ensure_data_directory(debug_mode=True)
    assert os.path.exists(DATA_DIR)

def test_save_and_load_logs(cleanup_data_dir):
    logs = [
        {"task": "test_task_1", "result": "success", "execution_time": 0.5, "timestamp": datetime.now().isoformat()},
        {"task": "test_task_2", "result": "failure", "execution_time": 1.0, "timestamp": datetime.now().isoformat()}
    ]
    save_logs(logs, debug_mode=True)
    
    loaded_logs = load_logs(debug_mode=True)
    assert len(loaded_logs) == 2
    assert loaded_logs[0]["task"] == "test_task_1"
    assert loaded_logs[1]["result"] == "failure"

def test_save_and_load_performance_data(cleanup_data_dir):
    performance_data = {
        "timestamp": datetime.now().isoformat(),
        "total_tasks": 10,
        "average_execution_time": 0.75,
        "success_rate": 0.9
    }
    save_performance_data(performance_data, debug_mode=True)
    
    loaded_data = load_performance_data(debug_mode=True)
    assert len(loaded_data) == 1
    assert loaded_data[0]["total_tasks"] == 10
    assert loaded_data[0]["success_rate"] == 0.9

def test_multiple_save_and_load_operations(cleanup_data_dir):
    save_logs([{"task": "task_1", "result": "success", "execution_time": 0.5, "timestamp": datetime.now().isoformat()}], debug_mode=True)
    save_logs([{"task": "task_2", "result": "failure", "execution_time": 1.0, "timestamp": datetime.now().isoformat()}], debug_mode=True)
    
    loaded_logs = load_logs(debug_mode=True)
    assert len(loaded_logs) == 2
    
    save_performance_data({"timestamp": datetime.now().isoformat(), "total_tasks": 5, "average_execution_time": 0.6}, debug_mode=True)
    save_performance_data({"timestamp": datetime.now().isoformat(), "total_tasks": 10, "average_execution_time": 0.7}, debug_mode=True)
    
    loaded_performance_data = load_performance_data(debug_mode=True)
    assert len(loaded_performance_data) == 2

def test_load_non_existent_data():
    for file in os.listdir(DATA_DIR):
        os.remove(os.path.join(DATA_DIR, file))
    
    assert load_logs(debug_mode=True) == []
    assert load_performance_data(debug_mode=True) == []

def test_save_invalid_data(cleanup_data_dir):
    with pytest.raises(TypeError):
        save_logs("invalid_data", debug_mode=True)
    
    with pytest.raises(TypeError):
        save_performance_data("invalid_data", debug_mode=True)

def test_data_persistence_across_sessions(cleanup_data_dir):
    # Session 1: Save data
    save_logs([{"task": "session_1_task", "result": "success", "execution_time": 0.5, "timestamp": datetime.now().isoformat()}], debug_mode=True)
    save_performance_data({"timestamp": datetime.now().isoformat(), "session": 1, "total_tasks": 5}, debug_mode=True)
    
    # Session 2: Load data and add more
    loaded_logs = load_logs(debug_mode=True)
    loaded_performance_data = load_performance_data(debug_mode=True)
    
    assert len(loaded_logs) == 1
    assert len(loaded_performance_data) == 1
    
    save_logs([{"task": "session_2_task", "result": "success", "execution_time": 0.7, "timestamp": datetime.now().isoformat()}], debug_mode=True)
    save_performance_data({"timestamp": datetime.now().isoformat(), "session": 2, "total_tasks": 10}, debug_mode=True)
    
    # Verify combined data
    final_logs = load_logs(debug_mode=True)
    final_performance_data = load_performance_data(debug_mode=True)
    
    assert len(final_logs) == 2
    assert len(final_performance_data) == 2
    assert final_logs[0]["task"] == "session_1_task"
    assert final_logs[1]["task"] == "session_2_task"
    assert final_performance_data[0]["session"] == 1
    assert final_performance_data[1]["session"] == 2

def test_clean_old_data(cleanup_data_dir):
    # Create some old data
    old_date = datetime.now() - timedelta(days=40)
    old_log_file = os.path.join(DATA_DIR, f"logs_{old_date.strftime('%Y%m%d_%H%M%S')}.json")
    old_performance_file = os.path.join(DATA_DIR, f"performance_{old_date.strftime('%Y%m%d_%H%M%S')}.json")
    
    with open(old_log_file, 'w') as f:
        json.dump({"timestamp": old_date.isoformat(), "logs": [{"task": "old_task", "result": "success"}]}, f)
    
    with open(old_performance_file, 'w') as f:
        json.dump({"timestamp": old_date.isoformat(), "total_tasks": 5}, f)
    
    # Create some recent data
    save_logs([{"task": "recent_task", "result": "success", "execution_time": 0.5, "timestamp": datetime.now().isoformat()}], debug_mode=True)
    save_performance_data({"timestamp": datetime.now().isoformat(), "total_tasks": 10}, debug_mode=True)
    
    # Clean old data
    clean_old_data(days_to_keep=30, debug_mode=True)
    
    # Check that old data is removed and recent data is kept
    current_files = os.listdir(DATA_DIR)
    assert not any(file.startswith(old_date.strftime('%Y%m%d')) for file in current_files)
    assert any(file.startswith(datetime.now().strftime('%Y%m%d')) for file in current_files)
    
    loaded_logs = load_logs(debug_mode=True)
    loaded_performance_data = load_performance_data(debug_mode=True)
    
    assert len(loaded_logs) == 1
    assert loaded_logs[0]["task"] == "recent_task"
    assert len(loaded_performance_data) == 1
    assert loaded_performance_data[0]["total_tasks"] == 10

def test_debug_mode_logging(capfd):
    save_logs([{"task": "debug_task", "result": "success", "execution_time": 0.5, "timestamp": datetime.now().isoformat()}], debug_mode=True)
    captured = capfd.readouterr()
    assert "Debug" in captured.out
    assert "Saved 1 log entries" in captured.out

if __name__ == "__main__":
    pytest.main([__file__])