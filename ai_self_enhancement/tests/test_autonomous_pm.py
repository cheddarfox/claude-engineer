import unittest
import os
import sys
import tempfile
from unittest.mock import patch

# Add the src directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from autonomous_pm import AutonomousProjectManager, Task

class TestAutonomousProjectManager(unittest.TestCase):
    def setUp(self):
        # Create a temporary file to use as a mock Kanban board
        self.temp_kanban = tempfile.NamedTemporaryFile(mode='w+', delete=False)
        self.temp_kanban.write("""# AI Self-Enhancement Project Kanban Board

## To Do
- [ ] Task 1 (Effort: 2, Value: 3, Dependencies: Task 2)
- [ ] Task 2 (Effort: 1, Value: 2)
- [ ] Task 3 (Effort: 3, Value: 5, Dependencies: Task 1,Task 2)

## In Progress

## Done
- [X] Task 0
""")
        self.temp_kanban.close()
        self.apm = AutonomousProjectManager(self.temp_kanban.name)

    def tearDown(self):
        # Remove the temporary file
        os.unlink(self.temp_kanban.name)

    def test_load_kanban(self):
        self.assertEqual(len(self.apm.tasks["To Do"]), 3)
        self.assertEqual(len(self.apm.tasks["In Progress"]), 0)
        self.assertEqual(len(self.apm.tasks["Done"]), 1)

    def test_parse_task(self):
        task_string = "Task 1 (Effort: 2, Value: 3, Dependencies: Task 2)"
        task = self.apm.parse_task(task_string)
        self.assertEqual(task.name, "Task 1")
        self.assertEqual(task.effort, 2)
        self.assertEqual(task.business_value, 3)
        self.assertEqual(task.dependencies, ["Task 2"])

    def test_prioritize_tasks(self):
        prioritized_tasks = self.apm.prioritize_tasks()
        self.assertEqual(len(prioritized_tasks), 1)
        self.assertEqual(prioritized_tasks[0].name, "Task 2")

    def test_select_next_task(self):
        next_task = self.apm.select_next_task()
        self.assertIsNotNone(next_task)
        self.assertEqual(next_task.name, "Task 2")

    def test_assign_task(self):
        task_to_assign = self.apm.tasks["To Do"][1]  # Task 2
        self.apm.assign_task(task_to_assign)
        self.assertEqual(len(self.apm.tasks["To Do"]), 2)
        self.assertEqual(len(self.apm.tasks["In Progress"]), 1)
        self.assertEqual(self.apm.tasks["In Progress"][0].name, "Task 2")

    def test_complete_task(self):
        task_to_complete = self.apm.tasks["To Do"][1]  # Task 2
        self.apm.assign_task(task_to_complete)
        self.apm.complete_task(task_to_complete)
        self.assertEqual(len(self.apm.tasks["To Do"]), 2)
        self.assertEqual(len(self.apm.tasks["In Progress"]), 0)
        self.assertEqual(len(self.apm.tasks["Done"]), 2)
        self.assertEqual(self.apm.tasks["Done"][1].name, "Task 2")

    @patch('logging.info')
    def test_run(self, mock_log):
        self.apm.run()
        self.assertEqual(len(self.apm.tasks["To Do"]), 0)
        self.assertEqual(len(self.apm.tasks["In Progress"]), 0)
        self.assertEqual(len(self.apm.tasks["Done"]), 4)
        mock_log.assert_called_with("No more tasks to process.")

if __name__ == '__main__':
    unittest.main()