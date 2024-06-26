"""
Self-Reflection Module

This module provides functionality for the AI system to reflect on its own performance,
analyze its capabilities, and suggest potential improvements.
"""

from time_utils import get_timestamp, get_time_difference

class SelfReflection:
    """
    A class to manage the AI system's self-reflection capabilities.

    This class allows the system to log its performance, analyze its efficiency,
    and suggest improvements based on its current capabilities and performance data.
    """

    def __init__(self, capability_registry):
        """
        Initialize the SelfReflection instance.

        Args:
            capability_registry (CapabilityRegistry): The system's capability registry.
        """
        self.capability_registry = capability_registry
        self.performance_log = []

    def log_performance(self, task, result, execution_time):
        """
        Log the performance of a completed task.

        Args:
            task (str): The name of the task performed.
            result: The result of the task execution.
            execution_time (float): The time taken to execute the task, in seconds.
        """
        self.performance_log.append({
            "task": task,
            "result": result,
            "execution_time": execution_time,
            "timestamp": get_timestamp()
        })

    def analyze_performance(self):
        """
        Analyze the system's performance based on logged data.

        Returns:
            str: A string containing the performance analysis report.
        """
        if not self.performance_log:
            return "No performance data available."

        total_tasks = len(self.performance_log)
        avg_execution_time = sum(log["execution_time"] for log in self.performance_log) / total_tasks

        analysis = f"Performance Analysis (as of {get_timestamp()}):\n"
        analysis += f"Total tasks completed: {total_tasks}\n"
        analysis += f"Average execution time: {avg_execution_time:.2f} seconds\n"

        # Identify areas for improvement
        slow_tasks = [log for log in self.performance_log if log["execution_time"] > avg_execution_time * 1.5]
        if slow_tasks:
            analysis += "\nAreas for improvement:\n"
            for task in slow_tasks:
                analysis += f"- Task '{task['task']}' took {task['execution_time']:.2f} seconds (above average)\n"

        # Calculate total runtime
        if len(self.performance_log) >= 2:
            start_time = self.performance_log[0]["timestamp"]
            end_time = self.performance_log[-1]["timestamp"]
            total_runtime = get_time_difference(start_time, end_time)
            analysis += f"\nTotal runtime: {total_runtime:.2f} seconds\n"

        return analysis

    def suggest_improvements(self):
        """
        Suggest potential improvements based on the system's current capabilities.

        Returns:
            list: A list of improvement suggestions.
        """
        available_capabilities = self.capability_registry.list_capabilities()
        missing_capabilities = [
            "natural_language_processing",
            "image_recognition",
            "speech_recognition",
            "machine_learning"
        ]

        suggestions = []
        for capability in missing_capabilities:
            if capability not in available_capabilities:
                suggestions.append(f"Consider adding '{capability}' to enhance overall functionality.")

        return suggestions if suggestions else ["No immediate suggestions for new capabilities."]

# Example usage:
# registry = CapabilityRegistry()
# self_reflection = SelfReflection(registry)
# self_reflection.log_performance("text_analysis", "Completed successfully", 0.5)
# print(self_reflection.analyze_performance())
# print(self_reflection.suggest_improvements())