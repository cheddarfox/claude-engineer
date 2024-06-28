import pytest
from unittest.mock import Mock, patch
from ai_self_enhancement.src.ai_core import AICore
from ai_self_enhancement.src.error_handling import AISelfEnhancementError

@pytest.fixture
def ai_core():
    with patch('ai_self_enhancement.src.ai_core.CapabilityRegistry') as mock_registry, \
         patch('ai_self_enhancement.src.ai_core.SelfReflection') as mock_reflection:
        core = AICore('test_dir', debug_mode=True)
        yield core

def test_ai_core_initialization(ai_core):
    assert ai_core.debug_mode == True
    assert ai_core.running == False
    assert isinstance(ai_core.performance_data, dict)

def test_start_and_stop(ai_core):
    with patch.object(ai_core, 'execute_task_cycle'), \
         patch.object(ai_core, 'perform_self_reflection'), \
         patch.object(ai_core, 'wait'):
        ai_core.start()
        assert ai_core.running == True
        ai_core.stop()
        assert ai_core.running == False

def test_main_loop_exception_handling(ai_core):
    with patch.object(ai_core, 'execute_task_cycle') as mock_execute, \
         patch.object(ai_core, 'perform_self_reflection') as mock_reflect, \
         patch.object(ai_core, 'wait') as mock_wait:
        mock_execute.side_effect = AISelfEnhancementError("Test error")
        ai_core.start()
        assert ai_core.running == False
        mock_execute.assert_called_once()
        mock_reflect.assert_not_called()
        mock_wait.assert_not_called()

def test_execute_task_cycle(ai_core):
    mock_capabilities = {'test_capability': 'Test description'}
    ai_core.capability_registry.list_capabilities.return_value = mock_capabilities
    with patch.object(ai_core, 'execute_capability') as mock_execute:
        mock_execute.return_value = {'result': 'success', 'execution_time': 1.0, 'category': 'test'}
        ai_core.execute_task_cycle()
        mock_execute.assert_called_once_with('test_capability')
        ai_core.self_reflection.log_performance.assert_called_once()

def test_execute_task_cycle_empty_capabilities(ai_core):
    ai_core.capability_registry.list_capabilities.return_value = {}
    ai_core.execute_task_cycle()
    ai_core.self_reflection.log_performance.assert_not_called()

def test_execute_capability(ai_core):
    ai_core.capability_registry.execute_capability.return_value = 'test_result'
    result = ai_core.execute_capability('test_capability')
    assert result['result'] == 'test_result'
    assert isinstance(result['execution_time'], float)
    assert result['category'] == 'capability_execution'

def test_execute_capability_error(ai_core):
    ai_core.capability_registry.execute_capability.side_effect = Exception('Test error')
    result = ai_core.execute_capability('test_capability')
    assert result['result'] is None
    assert isinstance(result['execution_time'], float)
    assert result['category'] == 'capability_execution'

def test_perform_self_reflection(ai_core):
    mock_analysis = {'test': 'analysis'}
    ai_core.self_reflection.analyze_performance.return_value = mock_analysis
    with patch.object(ai_core, 'act_on_insights') as mock_act:
        ai_core.perform_self_reflection()
        mock_act.assert_called_once_with(mock_analysis)

def test_act_on_insights(ai_core):
    mock_analysis = {
        'trend_analysis': {'trend_direction': 'decreasing', 'trend_strength': 0.6, 'slope': -0.1},
        'anomalies': [True, False, True],
        'performance_summary': {'mean': 1.0},
        'areas_for_improvement': [
            'Optimize performance for tasks: task1, task2',
            'Improve reliability of capabilities: cap1, cap2',
            'Consider adding new capabilities: new_cap'
        ]
    }
    with patch.object(ai_core, 'address_decreasing_performance') as mock_address_perf, \
         patch.object(ai_core, 'address_anomalies') as mock_address_anomalies, \
         patch.object(ai_core, 'optimize_slow_tasks') as mock_optimize, \
         patch.object(ai_core, 'improve_capability_reliability') as mock_improve, \
         patch.object(ai_core, 'consider_new_capabilities') as mock_consider:
        ai_core.act_on_insights(mock_analysis)
        mock_address_perf.assert_called_once_with(mock_analysis['trend_analysis'])
        mock_address_anomalies.assert_called_once_with(mock_analysis['performance_summary'], mock_analysis['anomalies'])
        mock_optimize.assert_called_once_with('Optimize performance for tasks: task1, task2')
        mock_improve.assert_called_once_with('Improve reliability of capabilities: cap1, cap2')
        mock_consider.assert_called_once_with('Consider adding new capabilities: new_cap')

def test_address_decreasing_performance(ai_core):
    trend = {'slope': -0.1, 'trend_strength': 0.7}
    with patch.object(ai_core, 'log_info') as mock_log:
        ai_core.address_decreasing_performance(trend)
        mock_log.assert_called_with(f"Addressing decreasing performance trend. Slope: {trend['slope']}")

def test_address_anomalies(ai_core):
    performance_summary = {'mean': 1.0}
    anomalies = [True, False, True]
    with patch.object(ai_core, 'log_info') as mock_log:
        ai_core.address_anomalies(performance_summary, anomalies)
        mock_log.assert_called_with(f"Addressing 2 detected anomalies")

def test_optimize_slow_tasks(ai_core):
    improvement = "Optimize performance for tasks: task1, task2"
    with patch.object(ai_core, 'log_info') as mock_log:
        ai_core.optimize_slow_tasks(improvement)
        mock_log.assert_called_with(f"Optimizing slow tasks: {improvement}")

def test_improve_capability_reliability(ai_core):
    improvement = "Improve reliability of capabilities: cap1, cap2"
    with patch.object(ai_core, 'log_info') as mock_log:
        ai_core.improve_capability_reliability(improvement)
        mock_log.assert_called_with(f"Improving capability reliability: {improvement}")

def test_consider_new_capabilities(ai_core):
    improvement = "Consider adding new capabilities: new_cap"
    with patch.object(ai_core, 'log_info') as mock_log:
        ai_core.consider_new_capabilities(improvement)
        mock_log.assert_called_with(f"Considering new capabilities: {improvement}")

def test_update_performance_data(ai_core):
    capability = "test_capability"
    task_result = {"result": "success", "execution_time": 1.0, "category": "test"}
    ai_core.update_performance_data(capability, task_result)
    assert capability in ai_core.performance_data
    assert ai_core.performance_data[capability][-1] == task_result

def test_wait(ai_core):
    with patch('ai_self_enhancement.src.ai_core.get_timestamp') as mock_timestamp, \
         patch('ai_self_enhancement.src.ai_core.get_time_difference') as mock_time_diff:
        mock_timestamp.side_effect = ["start_time", "end_time"]
        mock_time_diff.side_effect = [0, 5]  # First call returns 0, second call returns 5
        ai_core.wait(5)
        assert mock_timestamp.call_count == 2
        assert mock_time_diff.call_count == 2

if __name__ == "__main__":
    pytest.main([__file__])