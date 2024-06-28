"""
Autonomous Project Management Module

This module implements autonomous project management features for the AI Self-Enhancement System.
It includes capabilities for reading and parsing the Kanban board, task prioritization,
automatic task selection and assignment, progress tracking, and performance visualization.
"""

import os
import logging
from typing import List, Dict
import re
from time_utils import get_timestamp
from visualization import plot_task_completion_rate, plot_task_priority_distribution, plot_time_management, plot_project_progress

class Task:
    def __init__(self, name: str, dependencies: List[str] = None, effort: int = 1, business_value: int = 1):
        self.name = name
        self.dependencies = dependencies or []
        self.effort = effort
        self.business_value = business_value

    def __str__(self):
        return f"{self.name} (Effort: {self.effort}, Value: {self.business_value}, Dependencies: {','.join(self.dependencies)})"

class AutonomousProjectManager:
    def __init__(self, kanban_path: str):
        self.kanban_path = kanban_path
        self.tasks = {
            "To Do": [],
            "In Progress": [],
            "Done": []
        }
        self.project_logs = []
        self.total_tokens_used = 0
        self.load_kanban()

    def load_kanban(self):
        """Load and parse the Kanban board from the markdown file."""
        try:
            with open(self.kanban_path, 'r') as file:
                content = file.read()
                sections = content.split('##')[1:]  # Split by headers, ignore the first empty part
                for section in sections:
                    lines = section.strip().split('\n')
                    category = lines[0].strip()
                    tasks = [self.parse_task(line.strip()[4:]) for line in lines[1:] if line.strip().startswith('- [')]
                    self.tasks[category] = tasks
            logging.info("Kanban board loaded successfully.")
            self.log_action("load_kanban", "Kanban board loaded successfully")
        except Exception as e:
            logging.error(f"Error loading Kanban board: {str(e)}")
            self.log_action("load_kanban", f"Error loading Kanban board: {str(e)}", success=False)

    def parse_task(self, task_string: str) -> Task:
        """Parse a task string into a Task object."""
        # Regular expression to extract task metadata
        pattern = r'^(.*?)(?:\s+\(Effort:\s*(\d+),\s*Value:\s*(\d+)(?:,\s*Dependencies:\s*(.*))?\))?$'
        match = re.match(pattern, task_string)
        
        if match:
            name = match.group(1)
            effort = int(match.group(2)) if match.group(2) else 1
            business_value = int(match.group(3)) if match.group(3) else 1
            dependencies = match.group(4).split(',') if match.group(4) else []
            return Task(name, dependencies, effort, business_value)
        else:
            return Task(task_string)

    def prioritize_tasks(self) -> List[Task]:
        """Prioritize tasks based on dependencies, effort, and business value."""
        todo_tasks = self.tasks["To Do"]
        done_tasks = set(task.name for task in self.tasks["Done"])
        
        # Filter out tasks with unmet dependencies
        available_tasks = [task for task in todo_tasks if all(dep in done_tasks for dep in task.dependencies)]
        
        # Sort tasks by the ratio of business value to effort, in descending order
        prioritized_tasks = sorted(available_tasks, key=lambda t: t.business_value / t.effort, reverse=True)
        
        self.log_action("prioritize_tasks", f"Prioritized {len(prioritized_tasks)} tasks")
        return prioritized_tasks

    def select_next_task(self) -> Task:
        """Select the next task to work on based on priority."""
        prioritized_tasks = self.prioritize_tasks()
        next_task = prioritized_tasks[0] if prioritized_tasks else None
        if next_task:
            self.log_action("select_next_task", f"Selected task: {next_task.name}")
        else:
            self.log_action("select_next_task", "No task selected, no more tasks to process")
        return next_task

    def assign_task(self, task: Task):
        """Assign a task by moving it to the 'In Progress' column."""
        if task in self.tasks["To Do"]:
            self.tasks["To Do"].remove(task)
            self.tasks["In Progress"].append(task)
            self.update_kanban()
            logging.info(f"Task assigned: {task}")
            self.log_action("assign_task", f"Assigned task: {task.name}")
        else:
            logging.warning(f"Task not found in 'To Do' list: {task}")
            self.log_action("assign_task", f"Failed to assign task: {task.name}", success=False)

    def complete_task(self, task: Task):
        """Mark a task as complete by moving it to the 'Done' column."""
        if task in self.tasks["In Progress"]:
            self.tasks["In Progress"].remove(task)
            self.tasks["Done"].append(task)
            self.update_kanban()
            logging.info(f"Task completed: {task}")
            self.log_action("complete_task", f"Completed task: {task.name}")
        else:
            logging.warning(f"Task not found in 'In Progress' list: {task}")
            self.log_action("complete_task", f"Failed to complete task: {task.name}", success=False)

    def update_kanban(self):
        """Update the Kanban board markdown file with the current task status."""
        try:
            with open(self.kanban_path, 'w') as file:
                file.write("# AI Self-Enhancement Project Kanban Board\n\n")
                for category, tasks in self.tasks.items():
                    file.write(f"## {category}\n")
                    for task in tasks:
                        status = 'X' if category == 'Done' else ' '
                        file.write(f"- [{status}] {str(task)}\n")
                    file.write("\n")
            logging.info("Kanban board updated successfully.")
            self.log_action("update_kanban", "Kanban board updated successfully")
        except Exception as e:
            logging.error(f"Error updating Kanban board: {str(e)}")
            self.log_action("update_kanban", f"Error updating Kanban board: {str(e)}", success=False)

    def estimate_tokens(self, text: str) -> int:
        """Estimate the number of tokens in a given text."""
        # This is a very rough estimation. In practice, you'd use the model's tokenizer.
        return len(text.split())

    def log_action(self, action: str, description: str, success: bool = True):
        """Log a project management action."""
        tokens_used = self.estimate_tokens(action + description)
        self.total_tokens_used += tokens_used
        log_entry = {
            "timestamp": get_timestamp(),
            "action": action,
            "description": description,
            "success": success,
            "tokens_used": tokens_used
        }
        self.project_logs.append(log_entry)

    def get_project_logs(self) -> List[Dict]:
        """Retrieve the project logs for analysis."""
        return self.project_logs

    def generate_performance_visualizations(self):
        """Generate visualizations for project performance analysis."""
        # Task completion rate
        total_tasks = len(self.tasks["To Do"]) + len(self.tasks["In Progress"]) + len(self.tasks["Done"])
        completed_tasks = len(self.tasks["Done"])
        plot_task_completion_rate(completed_tasks, total_tasks)

        # Task priority distribution
        priority_counts = {
            "High": sum(1 for task in self.tasks["To Do"] if task.business_value / task.effort > 1),
            "Medium": sum(1 for task in self.tasks["To Do"] if task.business_value / task.effort == 1),
            "Low": sum(1 for task in self.tasks["To Do"] if task.business_value / task.effort < 1)
        }
        plot_task_priority_distribution(priority_counts)

        # Token usage over time
        timestamps = [log['timestamp'] for log in self.project_logs]
        token_usage = [log['tokens_used'] for log in self.project_logs]
        plot_project_progress(timestamps, token_usage, "Token Usage Over Time", "Tokens Used")

    def run(self):
        """Main loop for autonomous project management."""
        self.log_action("run", "Starting autonomous project management")
        while True:
            next_task = self.select_next_task()
            if next_task:
                self.assign_task(next_task)
                # TODO: Implement actual task execution logic
                # For now, we'll just mark the task as complete
                self.complete_task(next_task)
            else:
                logging.info("No more tasks to process.")
                self.log_action("run", "Completed all tasks, ending autonomous project management")
                break
        
        self.generate_performance_visualizations()
        logging.info(f"Total tokens used: {self.total_tokens_used}")

if __name__ == "__main__":
    kanban_path = os.path.join(os.path.dirname(__file__), '..', 'kanban-board.md')
    apm = AutonomousProjectManager(kanban_path)
    apm.run()