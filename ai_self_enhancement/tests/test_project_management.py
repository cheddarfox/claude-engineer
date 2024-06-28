import unittest
import sys
import os
from unittest.mock import MagicMock, patch

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import AISelfEnhancementSystem
from autonomous_pm import AutonomousProjectManager
from self_reflection import SelfReflection

class TestProjectManagement(unittest.TestCase):

    def setUp(self):
        self.ai_system = AISelfEnhancementSystem()
        self.ai_system.project_manager = MagicMock(spec=AutonomousProjectManager)
        self.ai_system.self_reflection = MagicMock(spec=SelfReflection)

    def test_run_autonomous_pm(self):
        # Mock project logs
        mock_logs = [
            {"timestamp": "2023-03-15T10:00:00", "action": "assign_task", "description": "Assigned task: Task 1"},
            {"timestamp": "2023-03-15T11:00:00", "action": "complete_task", "description": "Completed task: Task 1"},
        ]
        self.ai_system.project_manager.get_project_logs.return_value = mock_logs

        # Run the autonomous project management
        self.ai_system.run_autonomous_pm()

        # Assert that the project manager's run method was called
        self.ai_system.project_manager.run.assert_called_once()

        # Assert that the project logs were passed to the self-reflection module
        self.ai_system.self_reflection.log_project_management_performance.assert_called_once_with(mock_logs)

    def test_analyze_project_management_performance(self):
        # Mock analysis results
        mock_analysis = {
            "total_tasks_managed": 10,
            "task_completion_rate": 0.8,
            "prioritization_effectiveness": {"priority_adherence_rate": 0.9, "average_priority_score": 0.75},
            "areas_for_improvement": ["Improve task completion rate", "Refine priority scoring mechanism"]
        }
        self.ai_system.self_reflection.analyze_project_management_performance.return_value = mock_analysis

        # Capture the printed output
        with patch('builtins.print') as mock_print:
            self.ai_system.analyze_project_management_performance()

        # Assert that the analysis method was called
        self.ai_system.self_reflection.analyze_project_management_performance.assert_called_once()

        # Assert that the analysis results were printed
        mock_print.assert_any_call("\nProject Management Performance Analysis:")
        for key, value in mock_analysis.items():
            mock_print.assert_any_call(f"{key}: {value}")

if __name__ == '__main__':
    unittest.main()