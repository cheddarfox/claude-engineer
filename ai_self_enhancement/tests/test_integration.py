import pytest
from unittest.mock import patch, MagicMock
from ai_self_enhancement.src.ai_core import AICore
from ai_self_enhancement.src.capability_registry import CapabilityRegistry
from ai_self_enhancement.src.self_reflection import SelfReflection
from ai_self_enhancement.src.advanced_analytics import AdvancedAnalytics

@pytest.fixture
def mock_capability_dir(tmp_path):
    capability_dir = tmp_path / "capabilities"
    capability_dir.mkdir()
    (capability_dir / "test_capability.py").write_text("""
def test_function(x):
    return x * 2
""")
    return str(capability_dir)

@pytest.fixture
def ai_core(mock_capability_dir):
    return AICore(mock_capability_dir, debug_mode=True)

def test_ai_core_capability_registry_integration(ai_core):
    # Test that AICore correctly initializes and uses CapabilityRegistry
    assert isinstance(ai_core.capability_registry, CapabilityRegistry)
    capabilities = ai_core.capability_registry.list_capabilities()
    assert "test_capability.test_function" in capabilities

def test_ai_core_self_reflection_integration(ai_core):
    # Test that AICore correctly initializes and uses SelfReflection
    assert isinstance(ai_core.self_reflection, SelfReflection)
    
    # Simulate task execution and performance logging
    with patch.object(ai_core.capability_registry, 'execute_capability', return_value="test_result"):
        ai_core.execute_capability("test_capability.test_function")
    
    # Check that performance was logged
    assert len(ai_core.self_reflection.performance_log) > 0

def test_self_reflection_advanced_analytics_integration(ai_core):
    # Test that SelfReflection correctly uses AdvancedAnalytics
    assert isinstance(ai_core.self_reflection.advanced_analytics, AdvancedAnalytics)
    
    # Simulate performance data
    ai_core.self_reflection.log_performance("test_task", "success", 1.0)
    
    # Perform analysis
    with patch.object(AdvancedAnalytics, 'analyze_trend'), \
         patch.object(AdvancedAnalytics, 'detect_anomalies'), \
         patch.object(AdvancedAnalytics, 'forecast_performance'):
        analysis = ai_core.self_reflection.analyze_performance()
    
    # Check that advanced analytics methods were called
    AdvancedAnalytics.analyze_trend.assert_called()
    AdvancedAnalytics.detect_anomalies.assert_called()
    AdvancedAnalytics.forecast_performance.assert_called()

def test_end_to_end_self_enhancement_process(ai_core):
    # Simulate multiple task executions
    with patch.object(ai_core.capability_registry, 'execute_capability', return_value="test_result"):
        for _ in range(5):
            ai_core.execute_capability("test_capability.test_function")
    
    # Perform self-reflection
    with patch.object(ai_core, 'act_on_insights') as mock_act_on_insights:
        ai_core.perform_self_reflection()
    
    # Check that insights were generated and acted upon
    mock_act_on_insights.assert_called()
    
    # Generate and check report
    report = ai_core.self_reflection.generate_report()
    assert isinstance(report, str)
    assert "Performance Report" in report

if __name__ == "__main__":
    pytest.main([__file__])