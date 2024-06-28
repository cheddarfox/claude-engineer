"""
Self-Reflection Module

This module provides functionality for the AI system to reflect on its own performance,
analyze its capabilities, and suggest potential improvements.
"""

from typing import List, Dict, Any
from time_utils import get_timestamp

class SelfReflection:
    def __init__(self, capability_registry):
        self.capability_registry = capability_registry
        self.performance_logs = []
        self.project_management_logs = []

    def log_performance(self, task_name: str, result: Any, execution_time: float):
        """Log the performance of a completed task."""
        log_entry = {
            "timestamp": get_timestamp(),
            "task_name": task_name,
            "result": result,
            "execution_time": execution_time
        }
        self.performance_logs.append(log_entry)

    def log_project_management_performance(self, project_logs: List[Dict[str, Any]]):
        """Log the performance of project management activities."""
        self.project_management_logs.extend(project_logs)

    def analyze_performance(self) -> Dict[str, Any]:
        """Analyze the overall performance of the system."""
        if not self.performance_logs:
            return {"message": "No performance data available."}

        total_tasks = len(self.performance_logs)
        total_execution_time = sum(log["execution_time"] for log in self.performance_logs)
        avg_execution_time = total_execution_time / total_tasks

        return {
            "total_tasks": total_tasks,
            "total_execution_time": total_execution_time,
            "average_execution_time": avg_execution_time
        }

    def analyze_project_management_performance(self) -> Dict[str, Any]:
        """Analyze the performance of project management activities."""
        if not self.project_management_logs:
            return {"message": "No project management data available."}

        total_tasks = len(self.project_management_logs)
        completed_tasks = sum(1 for log in self.project_management_logs if log.get("action") == "complete_task")
        
        priority_distribution = {
            "High": 0,
            "Medium": 0,
            "Low": 0
        }
        
        progress_over_time = []
        token_usage_over_time = []
        total_tokens_used = 0

        for log in self.project_management_logs:
            # Update priority distribution
            priority = log.get("priority", "Medium")
            priority_distribution[priority] += 1

            # Update progress and token usage over time
            progress_over_time.append({
                "timestamp": log["timestamp"],
                "progress": completed_tasks / total_tasks * 100
            })
            
            tokens_used = log.get("tokens_used", 0)
            total_tokens_used += tokens_used
            token_usage_over_time.append({
                "timestamp": log["timestamp"],
                "tokens": tokens_used
            })

        return {
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "completion_rate": completed_tasks / total_tasks,
            "priority_distribution": priority_distribution,
            "progress_over_time": progress_over_time,
            "token_usage_over_time": token_usage_over_time,
            "total_tokens_used": total_tokens_used
        }

    def suggest_improvements(self) -> List[str]:
        """Generate improvement suggestions based on performance analysis."""
        performance_analysis = self.analyze_performance()
        project_management_analysis = self.analyze_project_management_performance()

        suggestions = []

        if performance_analysis.get("average_execution_time", 0) > 1.0:
            suggestions.append("Consider optimizing task execution for better performance.")

        if project_management_analysis.get("completion_rate", 0) < 0.8:
            suggestions.append("Improve task completion rate in project management.")

        if project_management_analysis.get("total_tokens_used", 0) > 10000:
            suggestions.append("Look into reducing token usage for more efficient operations.")

        return suggestions

# Add any additional methods or classes as needed