import pytest
import os
import json
from ai_self_enhancement.src.data_persistence import (
    ensure_data_directory,
    save_logs,
    load_logs,
    save_performance_data,
    load_performance_data,
    DATA_DIR
)

@pytest.fixture
def cleanup_data_dir():
    yield
    for file in os.listdir(DATA_DIR):
        os.remove(os.path.join(DATA_DIR, file))

def test_ensure_data_directory():
    ensure_data_directory()
    assert os.path.exists(DATA_DIR)

def test_save_and_load_logs(cleanup_data_dir):
    logs = [
        {"task": "test_task_1", "result": "success", "execution_time": 0.5},
        {"task": "test_task_2", "result": "failure", "execution_time": 1.0}
    ]
    save_logs(logs)
    
    loaded_logs = load_logs()
    assert len(loaded_logs) == 2
    assert loaded_logs[0]["task"] == "test_task_1"
    assert loaded_logs[1]["result"] == "failure"

def test_save_and_load_performance_data(cleanup_data_dir):
    performance_data = {
        "total_tasks": 10,
        "average_execution_time": 0.75,
        "success_rate": 0.9
    }
    save_performance_data(performance_data)
    
    loaded_data = load_performance_data()
    assert len(loaded_data) == 1
    assert loaded_data[0]["total_tasks"] == 10
    assert loaded_data[0]["success_rate"] == 0.9

def test_multiple_save_and_load_operations(cleanup_data_dir):
    save_logs([{"task": "task_1", "result": "success", "execution_time": 0.5}])
    save_logs([{"task": "task_2", "result": "failure", "execution_time": 1.0}])
    
    loaded_logs = load_logs()
    assert len(loaded_logs) == 2
    
    save_performance_data({"total_tasks": 5, "average_execution_time": 0.6})
    save_performance_data({"total_tasks": 10, "average_execution_time": 0.7})
    
    loaded_performance_data = load_performance_data()
    assert len(loaded_performance_data) == 2

def test_load_non_existent_data():
    for file in os.listdir(DATA_DIR):
        os.remove(os.path.join(DATA_DIR, file))
    
    assert load_logs() == []
    assert load_performance_data() == []

def test_save_invalid_data(cleanup_data_dir):
    with pytest.raises(TypeError):
        save_logs("invalid_data")
    
    with pytest.raises(TypeError):
        save_performance_data("invalid_data")

def test_data_persistence_across_sessions(cleanup_data_dir):
    # Session 1: Save data
    save_logs([{"task": "session_1_task", "result": "success", "execution_time": 0.5}])
    save_performance_data({"session": 1, "total_tasks": 5})
    
    # Session 2: Load data and add more
    loaded_logs = load_logs()
    loaded_performance_data = load_performance_data()
    
    assert len(loaded_logs) == 1
    assert len(loaded_performance_data) == 1
    
    save_logs([{"task": "session_2_task", "result": "success", "execution_time": 0.7}])
    save_performance_data({"session": 2, "total_tasks": 10})
    
    # Verify combined data
    final_logs = load_logs()
    final_performance_data = load_performance_data()
    
    assert len(final_logs) == 2
    assert len(final_performance_data) == 2
    assert final_logs[0]["task"] == "session_1_task"
    assert final_logs[1]["task"] == "session_2_task"
    assert final_performance_data[0]["session"] == 1
    assert final_performance_data[1]["session"] == 2