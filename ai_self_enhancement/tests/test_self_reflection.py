import pytest
from unittest.mock import Mock
from ai_self_enhancement.src.self_reflection import SelfReflection
from ai_self_enhancement.src.error_handling import SelfReflectionError

@pytest.fixture
def mock_capability_registry():
    return Mock()

@pytest.fixture
def self_reflection(mock_capability_registry):
    return SelfReflection(mock_capability_registry)

def test_self_reflection_initialization(self_reflection):
    assert len(self_reflection.performance_log) == 0

def test_log_performance(self_reflection):
    self_reflection.log_performance("test_task", "success", 1.5)
    assert len(self_reflection.performance_log) == 1
    log_entry = self_reflection.performance_log[0]
    assert log_entry["task"] == "test_task"
    assert log_entry["result"] == "success"
    assert log_entry["execution_time"] == 1.5
    assert "timestamp" in log_entry

def test_log_performance_invalid_input(self_reflection):
    with pytest.raises(SelfReflectionError):
        self_reflection.log_performance("", "result", 1.0)
    with pytest.raises(SelfReflectionError):
        self_reflection.log_performance("task", "result", -1.0)

def test_analyze_performance_no_data(self_reflection):
    analysis = self_reflection.analyze_performance()
    assert analysis == "No performance data available."

def test_analyze_performance_with_data(self_reflection):
    self_reflection.log_performance("task1", "success", 1.0)
    self_reflection.log_performance("task2", "success", 2.0)
    self_reflection.log_performance("task3", "success", 3.0)
    
    analysis = self_reflection.analyze_performance()
    assert "Performance Analysis" in analysis
    assert "Total tasks completed: 3" in analysis
    assert "Average execution time: 2.00 seconds" in analysis

def test_analyze_performance_with_slow_tasks(self_reflection):
    self_reflection.log_performance("fast_task", "success", 1.0)
    self_reflection.log_performance("slow_task", "success", 5.0)
    
    analysis = self_reflection.analyze_performance()
    assert "Areas for improvement" in analysis
    assert "slow_task" in analysis

def test_suggest_improvements(self_reflection, mock_capability_registry):
    mock_capability_registry.list_capabilities.return_value = ["existing_capability"]
    suggestions = self_reflection.suggest_improvements()
    
    assert len(suggestions) > 0
    assert any("natural_language_processing" in suggestion for suggestion in suggestions)
    assert any("image_recognition" in suggestion for suggestion in suggestions)
    assert any("speech_recognition" in suggestion for suggestion in suggestions)
    assert any("machine_learning" in suggestion for suggestion in suggestions)

def test_suggest_improvements_all_capabilities_present(self_reflection, mock_capability_registry):
    mock_capability_registry.list_capabilities.return_value = [
        "natural_language_processing",
        "image_recognition",
        "speech_recognition",
        "machine_learning"
    ]
    suggestions = self_reflection.suggest_improvements()
    
    assert len(suggestions) == 1
    assert suggestions[0] == "No immediate suggestions for new capabilities."

def test_suggest_improvements_error_handling(self_reflection, mock_capability_registry):
    mock_capability_registry.list_capabilities.side_effect = Exception("Registry error")
    
    with pytest.raises(SelfReflectionError):
        self_reflection.suggest_improvements()