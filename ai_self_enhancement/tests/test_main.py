import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from main import AISelfEnhancementSystem

class TestAISelfEnhancementSystem(unittest.TestCase):

    def setUp(self):
        self.ai_system = AISelfEnhancementSystem()

    @patch('main.plot_task_completion_rate')
    @patch('main.plot_task_priority_distribution')
    @patch('main.plot_progress_over_time')
    def test_display_pm_visualizations(self, mock_plot_progress, mock_plot_priority, mock_plot_completion):
        analysis = {
            'completed_tasks': 5,
            'total_tasks': 10,
            'priority_distribution': {'High': 3, 'Medium': 5, 'Low': 2},
            'progress_over_time': [
                {'timestamp': '2023-05-01T10:00:00', 'progress': 20},
                {'timestamp': '2023-05-02T10:00:00', 'progress': 50},
                {'timestamp': '2023-05-03T10:00:00', 'progress': 80}
            ],
            'token_usage_over_time': [
                {'timestamp': '2023-05-01T10:00:00', 'tokens': 100},
                {'timestamp': '2023-05-02T10:00:00', 'tokens': 250},
                {'timestamp': '2023-05-03T10:00:00', 'tokens': 400}
            ],
            'total_tokens_used': 750
        }

        self.ai_system.display_pm_visualizations(analysis)

        mock_plot_completion.assert_called_once_with(5, 10)
        mock_plot_priority.assert_called_once_with({'High': 3, 'Medium': 5, 'Low': 2})
        self.assertEqual(mock_plot_progress.call_count, 2)  # Called for both progress and token usage

    @patch('main.SelfReflection')
    def test_analyze_project_management_performance(self, mock_self_reflection):
        mock_analysis = {
            'completed_tasks': 5,
            'total_tasks': 10,
            'priority_distribution': {'High': 3, 'Medium': 5, 'Low': 2},
            'progress_over_time': [],
            'token_usage_over_time': [],
            'total_tokens_used': 750
        }
        mock_self_reflection.return_value.analyze_project_management_performance.return_value = mock_analysis

        with patch.object(self.ai_system, 'display_pm_visualizations') as mock_display:
            self.ai_system.analyze_project_management_performance()
            mock_display.assert_called_once_with(mock_analysis)

if __name__ == '__main__':
    unittest.main()