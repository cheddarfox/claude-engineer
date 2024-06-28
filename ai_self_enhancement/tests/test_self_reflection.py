import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from ai_self_enhancement.src.self_reflection import SelfReflection
from ai_self_enhancement.src.error_handling import SelfReflectionError

@pytest.fixture
def mock_capability_registry():
    registry = Mock()
    registry.list_capabilities.return_value = {"capability1": "Description 1", "capability2": "Description 2"}
    return registry

@pytest.fixture
def mock_advanced_analytics():
    analytics = Mock()
    analytics.analyze_trend.return_value = {"trend_direction": "increasing", "trend_strength": 0.8}
    analytics.detect_anomalies.return_value = [False, True, False]
    analytics.forecast_performance.return_value = [1.1, 1.2, 1.3]
    analytics.performance_summary.return_value = {"mean": 1.0, "median": 0.9, "std_dev": 0.2}
    return analytics

@pytest.fixture
def self_reflection(mock_capability_registry, mock_advanced_analytics):
    reflection = SelfReflection(mock_capability_registry, debug_mode=True)
    reflection.advanced_analytics = mock_advanced_analytics
    return reflection

def test_self_reflection_initialization(self_reflection):
    assert isinstance(self_reflection.performance_log, list)
    assert self_reflection.debug_mode == True

def test_log_performance(self_reflection):
    self_reflection.log_performance("test_task", "success", 1.5, "test_category")
    assert len(self_reflection.performance_log) == 1
    log_entry = self_reflection.performance_log[0]
    assert log_entry["task"] == "test_task"
    assert log_entry["result"] == "success"
    assert log_entry["execution_time"] == 1.5
    assert log_entry["category"] == "test_category"
    assert "timestamp" in log_entry

def test_log_performance_invalid_input(self_reflection):
    with pytest.raises(SelfReflectionError):
        self_reflection.log_performance("", "result", 1.0)
    with pytest.raises(SelfReflectionError):
        self_reflection.log_performance("task", "result", -1.0)

@patch('ai_self_enhancement.src.self_reflection.load_logs')
def test_analyze_performance_no_data(mock_load_logs, self_reflection):
    mock_load_logs.return_value = []
    analysis = self_reflection.analyze_performance()
    assert analysis["message"] == "No performance data available."

@patch('ai_self_enhancement.src.self_reflection.load_logs')
def test_analyze_performance_with_data(mock_load_logs, self_reflection):
    mock_logs = [
        {"task": "task1", "result": "success", "execution_time": 1.0, "timestamp": datetime.now().isoformat()},
        {"task": "task2", "result": "success", "execution_time": 2.0, "timestamp": datetime.now().isoformat()},
        {"task": "task3", "result": "failure", "execution_time": 3.0, "timestamp": datetime.now().isoformat()}
    ]
    mock_load_logs.return_value = mock_logs
    
    analysis = self_reflection.analyze_performance()
    assert "timestamp" in analysis
    assert analysis["total_tasks"] == 3
    assert "performance_summary" in analysis
    assert "trend_analysis" in analysis
    assert "anomalies" in analysis
    assert "forecast" in analysis
    assert "task_categories" in analysis
    assert "capability_usage" in analysis
    assert "areas_for_improvement" in analysis

def test_advanced_analytics_integration(self_reflection):
    logs = [
        {"task": "task1", "result": "success", "execution_time": 1.0, "timestamp": datetime.now().isoformat()},
        {"task": "task2", "result": "success", "execution_time": 2.0, "timestamp": datetime.now().isoformat()},
        {"task": "task3", "result": "failure", "execution_time": 3.0, "timestamp": datetime.now().isoformat()}
    ]
    analysis = self_reflection.analyze_performance()
    
    assert self_reflection.advanced_analytics.analyze_trend.called
    assert self_reflection.advanced_analytics.detect_anomalies.called
    assert self_reflection.advanced_analytics.forecast_performance.called
    assert self_reflection.advanced_analytics.performance_summary.called

def test_analyze_task_categories(self_reflection):
    logs = [
        {"task": "task1", "result": "success", "execution_time": 1.0, "category": "category1"},
        {"task": "task2", "result": "success", "execution_time": 2.0, "category": "category1"},
        {"task": "task3", "result": "failure", "execution_time": 3.0, "category": "category2"}
    ]
    categories = self_reflection._analyze_task_categories(logs)
    assert "category1" in categories
    assert "category2" in categories
    assert categories["category1"]["total_tasks"] == 2
    assert categories["category2"]["total_tasks"] == 1

@patch('ai_self_enhancement.src.self_reflection.load_logs')
def test_generate_report(mock_load_logs, self_reflection):
    mock_logs = [
        {"task": "task1", "result": "success", "execution_time": 1.0, "timestamp": datetime.now().isoformat(), "category": "category1"},
        {"task": "task2", "result": "success", "execution_time": 2.0, "timestamp": datetime.now().isoformat(), "category": "category1"},
        {"task": "task3", "result": "failure", "execution_time": 3.0, "timestamp": datetime.now().isoformat(), "category": "category2"}
    ]
    mock_load_logs.return_value = mock_logs
    
    report = self_reflection.generate_report()
    assert isinstance(report, str)
    assert "Performance Report" in report
    assert "Overall Statistics" in report
    assert "Performance Trend" in report
    assert "Anomalies" in report
    assert "Performance Forecast" in report
    assert "Task Categories" in report
    assert "Capability Usage" in report
    assert "Areas for Improvement" in report

def test_identify_areas_for_improvement(self_reflection):
    logs = [
        {"task": "fast_task", "result": "success", "execution_time": 1.0},
        {"task": "slow_task", "result": "success", "execution_time": 5.0},
        {"task": "capability1", "result": "success", "execution_time": 1.0},
        {"task": "capability1", "result": "failure", "execution_time": 1.0},
        {"task": "capability2", "result": "success", "execution_time": 1.0},
    ]
    improvements = self_reflection._identify_areas_for_improvement(logs)
    assert any("slow_task" in improvement for improvement in improvements)
    assert any("capability1" in improvement for improvement in improvements)
    assert any("new capabilities" in improvement for improvement in improvements)

@patch('ai_self_enhancement.src.self_reflection.load_logs')
def test_error_handling_in_performance_analysis(mock_load_logs, self_reflection):
    mock_load_logs.side_effect = Exception("Test error")
    
    with pytest.raises(SelfReflectionError):
        self_reflection.analyze_performance()

@patch('ai_self_enhancement.src.self_reflection.log_debug')
def test_debug_mode(mock_log_debug, self_reflection):
    self_reflection.log_performance("debug_task", "success", 1.0)
    assert mock_log_debug.called

if __name__ == "__main__":
    pytest.main([__file__])